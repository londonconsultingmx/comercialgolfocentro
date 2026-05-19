#!/usr/bin/env python3
"""
========================================================================
ANALYZE — Inteligencia comercial sobre posts de Whitepaper para LCG
========================================================================
Toma output/posts/*.json (extraídos por extract_whitepaper.py) y produce:

    output/tagged_index.json    — Catálogo con tags por post
    output/categorias.html/.txt — Resumen por sector + tipo de evento
    output/zona.html/.txt       — Deep dive de los 11 estados de la zona
                                  Sur-Centro-Golfo, con notas comerciales
                                  por estado y por sector.

Uso:
    python analyze.py
========================================================================
"""

import json
import re
import html
from pathlib import Path
from collections import Counter, defaultdict

OUT = Path("./output")
POSTS_DIR = OUT / "posts"

# ========================================================================
# TAXONOMÍA — Estados de la zona LCG Sur-Centro-Golfo
# ========================================================================
ZONA_ESTADOS = [
    "Puebla", "Quintana Roo", "Veracruz", "Yucatán", "Hidalgo",
    "Campeche", "Tabasco", "Guerrero", "Chiapas", "Oaxaca",
]

# Patrones para detectar estados (incluye ciudades importantes)
ESTADOS_PATTERNS = {
    "Aguascalientes": [r"\bAguascalientes\b"],
    "Baja California": [r"\bBaja California\b(?! Sur)", r"\bTijuana\b", r"\bMexicali\b", r"\bEnsenada\b"],
    "Baja California Sur": [r"\bBaja California Sur\b", r"\bLa Paz\b", r"\bLos Cabos\b"],
    "Campeche": [r"\bCampeche\b", r"\bCalkiní\b", r"\bChampotón\b", r"\bHopelchén\b"],
    "Chiapas": [r"\bChiapas\b", r"\bTuxtla\b", r"\bSan Cristóbal\b", r"\bTapachula\b", r"\bSoconusco\b"],
    "Chihuahua": [r"\bChihuahua\b", r"\bCiudad Juárez\b", r"\bDelicias\b"],
    "CDMX": [r"\bCDMX\b", r"\bCiudad de México\b", r"\bDistrito Federal\b"],
    "Coahuila": [r"\bCoahuila\b", r"\bSaltillo\b", r"\bTorreón\b", r"\bMonclova\b"],
    "Colima": [r"\bColima\b", r"\bManzanillo\b"],
    "Durango": [r"\bDurango\b", r"\bGómez Palacio\b"],
    "Estado de México": [r"\bEstado de México\b", r"\bEdomex\b", r"\bToluca\b", r"\bEcatepec\b", r"\bNaucalpan\b"],
    "Guanajuato": [r"\bGuanajuato\b", r"\bLeón\b", r"\bCelaya\b", r"\bIrapuato\b", r"\bSan Miguel de Allende\b"],
    "Guerrero": [r"\bGuerrero\b", r"\bAcapulco\b", r"\bIxtapa\b", r"\bZihuatanejo\b", r"\bTaxco\b"],
    "Hidalgo": [r"\bHidalgo\b", r"\bPachuca\b", r"\bTula\b", r"\bTulancingo\b"],
    "Jalisco": [r"\bJalisco\b", r"\bGuadalajara\b", r"\bPuerto Vallarta\b", r"\bTlaquepaque\b", r"\bZapopan\b", r"\bTequila\b"],
    "Michoacán": [r"\bMichoacán\b", r"\bMorelia\b", r"\bUruapan\b", r"\bLázaro Cárdenas\b"],
    "Morelos": [r"\bMorelos\b", r"\bCuernavaca\b"],
    "Nayarit": [r"\bNayarit\b", r"\bTepic\b", r"\bRiviera Nayarit\b"],
    "Nuevo León": [r"\bNuevo León\b", r"\bMonterrey\b", r"\bApodaca\b", r"\bSan Pedro\b(?: Garza)?", r"\bSan Nicolás\b"],
    "Oaxaca": [r"\bOaxaca\b", r"\bHuatulco\b", r"\bPluma Hidalgo\b", r"\bSierra Sur\b"],
    "Puebla": [r"\bPuebla\b", r"\bCholula\b", r"\bTehuacán\b"],
    "Querétaro": [r"\bQuerétaro\b", r"\bEl Marqués\b"],
    "Quintana Roo": [r"\bQuintana Roo\b", r"\bCancún\b", r"\bPlaya del Carmen\b", r"\bRiviera Maya\b", r"\bTulum\b", r"\bChetumal\b", r"\bIsla Mujeres\b"],
    "San Luis Potosí": [r"\bSan Luis Potosí\b", r"\bSLP\b"],
    "Sinaloa": [r"\bSinaloa\b", r"\bCuliacán\b", r"\bMazatlán\b"],
    "Sonora": [r"\bSonora\b", r"\bHermosillo\b", r"\bNogales\b", r"\bGuaymas\b"],
    "Tabasco": [r"\bTabasco\b", r"\bVillahermosa\b"],
    "Tamaulipas": [r"\bTamaulipas\b", r"\bTampico\b", r"\bReynosa\b", r"\bNuevo Laredo\b", r"\bMatamoros\b"],
    "Tlaxcala": [r"\bTlaxcala\b"],
    "Veracruz": [r"\bVeracruz\b", r"\bXalapa\b", r"\bCoatzacoalcos\b", r"\bTuxpan\b", r"\bMinatitlán\b", r"\bCórdoba\b", r"\bOrizaba\b", r"\bPoza Rica\b", r"\bCoatepec\b", r"\bPapantla\b"],
    "Yucatán": [r"\bYucatán\b", r"\bMérida\b", r"\bValladolid\b", r"\bProgreso\b"],
    "Zacatecas": [r"\bZacatecas\b", r"\bFresnillo\b"],
}

# ========================================================================
# TAXONOMÍA — Sectores comerciales (relevantes para LCG)
# ========================================================================
SECTORES = {
    "Alimentos y Bebidas": [
        r"\b(Coca[- ]Cola|Pepsi|Bimbo|Maseca|Gruma|La Costeña|Sigma|Lala|Alpura|Bachoco|Bepensa|Modelo|Heineken|Ab InBev|Constellation Brands)\b",
        r"\b(refresco|cerveza|tequila|mezcal|vino|lácteo|panadería|panificadora|alimentos|bebida|alimentaria|gastronomía)\b",
        r"\b(restaurante|CANIRAC)\b",
    ],
    "Retail / Comercio": [
        r"\b(Chedraui|Soriana|Walmart|Costco|Sam's|Liverpool|Suburbia|Palacio de Hierro|Sanborns|Sears|HEB|7-?Eleven|OXXO|Comercial Mexicana|Fresko|Coppel|Elektra)\b",
        r"\b(autoservicio|tienda departamental|cadena de tiendas|retail|e-?commerce|comercio electrónico|Mercado Libre|MercadoLibre)\b",
    ],
    "Turismo / Hospitalidad": [
        r"\b(Vidanta|Xcaret|Palace|Posadas|RIU|Iberostar|Barceló|Marriott|Hilton|Hyatt|Fiesta Americana|Camino Real|Krystal|City Express)\b",
        r"\b(turismo|hotel|hospedaje|resort|todo incluido|hospitalidad|Tianguis Turístico|sectur)\b",
    ],
    "Automotriz": [
        r"\b(BMW|Audi|Ford|General Motors|GM|Stellantis|Nissan|Toyota|Honda|Mazda|Volkswagen|VW|Kia|Hyundai|Tesla|BYD|Chery|JAC|Geely|MG|Great Wall|Volvo|Mercedes-?Benz)\b",
        r"\b(ensambladora|autopartes|OEM|Tier 1|Tier 2|automotriz|automotor|ensamblaje|vehículo|camionetas?|sedan|crossover|EV|eléctric)\b",
        r"\b(plantas? armadora|distribuidor automotriz|agencia automotriz)\b",
    ],
    "Banca / Finanzas / Seguros": [
        r"\b(BBVA|Banamex|Citibanamex|Santander|Banorte|Inbursa|HSBC|Scotiabank|Banregio|Banco Azteca|Banco Sabadell|Banco del Bajío|BanCoppel|BanBajío|Compartamos|Mifel|Multiva)\b",
        r"\b(fintech|neobanco|Klar|Nu|Konfío|Stori|Cuenca|Albo|Yave|Klar)\b",
        r"\b(seguros|aseguradora|GNP|MetLife|Mapfre|Quálitas|Axa)\b",
        r"\b(crédito|préstamo|hipoteca|leasing|factoraje)\b",
        r"\b(BMV|Bolsa Mexicana|BIVA|CNBV|Banxico)\b",
    ],
    "Energía / Petroquímica": [
        r"\b(Pemex|CFE|Iberdrola|Engie|Sempra|IEnova|TC Energía|Bal Ondeo|Naturgy)\b",
        r"\b(petroquímica|refinería|gas natural|hidrocarburo|gasolinera|estación de servicio)\b",
        r"\b(energía solar|eólico|renovable|fotovoltaic|parque solar|parque eólico)\b",
        r"\b(SHCP|CRE|CNH)\b",
    ],
    "Real Estate / Construcción": [
        r"\b(Cemex|Holcim|Cementos Moctezuma|Cementos Cruz Azul|GCC|Cementos Chihuahua|Apasco)\b",
        r"\b(ARA|GEO|Homex|Sare|Vinte|Javer|Cadu|Ruba)\b",
        r"\b(Fibra|FIBRA|Funo|Macquarie|Terrafina|Hotel Fibra)\b",
        r"\b(inmobiliari[ao]|real estate|construcción|vivienda|residencial|departamento)\b",
    ],
    "Tecnología / Telecom": [
        r"\b(Telmex|Telcel|AT&T|Movistar|Megacable|Izzi|Totalplay|Telefónica)\b",
        r"\b(Google|Microsoft|Amazon Web Services|AWS|IBM|SAP|Oracle|Salesforce|Adobe)\b",
        r"\b(startup|tech|software|app móvil|SaaS|inteligencia artificial|IA|fintech|edtech|insurtech|proptech|cleantech|biotech)\b",
        r"\b(Series [A-D]|ronda de capital|venture capital|VC|capital semilla|seed|Kaszek|Mountain Nazca|Dalus|Wollef|Cometa)\b",
    ],
    "Salud / Farmacéutica": [
        r"\b(Genomma|Pisa|Sanfer|Carnot|Liomont|Stendhal|Bayer|Pfizer|Roche|Sanofi|Merck|AstraZeneca|Novartis|Lilly|GSK|Johnson)\b",
        r"\b(Farmacias del Ahorro|Farmacias Guadalajara|Farmacias Benavides|Farmacias San Pablo|Walmart Farmacia)\b",
        r"\b(hospital|clínica|farmacéutic|laboratorio|biotecnología|salud)\b",
    ],
    "Agroindustria": [
        r"\b(agropecuario|agrícola|ganadero|granja|cultivo|cosecha|exportación agrícola)\b",
        r"\b(aguacate|café|cacao|agave|caña de azúcar|maíz|trigo|sorgo|tomate|berry|frutícola)\b",
        r"\b(SADER|SAGARPA|FIRA)\b",
    ],
    "Logística / Transporte": [
        r"\b(DHL|FedEx|Estafeta|UPS|Redpack|Paquetexpress)\b",
        r"\b(Aeroméxico|Volaris|Viva Aerobus|Magnicharters|VivaAerobus)\b",
        r"\b(logística|transporte|fletes|paquetería|naviera|puerto|aeropuerto|ferroviario|tren|Ferromex|Kansas City Southern)\b",
        r"\b(Tren Maya|Tren Interurbano)\b",
    ],
    "Manufactura Industrial": [
        r"\b(manufactura|maquiladora|IMMEX|planta industrial|fábrica|nearshoring|relocalización)\b",
        r"\b(AHMSA|Ternium|ArcelorMittal|Deacero|Grupo México|GMexico|Industrias Peñoles|Peñoles|Tetra Pak)\b",
        r"\b(siderurgia|acero|aluminio|cobre|zinc|minería)\b",
    ],
    "Medios / Entretenimiento": [
        r"\b(Televisa|TV Azteca|Cinépolis|Cinemex|Netflix|Disney|Warner|HBO|Spotify|YouTube)\b",
        r"\b(medios de comunicación|televisión|streaming|cinematográfic|entretenimiento)\b",
    ],
    "Educación": [
        r"\b(Tec de Monterrey|ITESM|Tecnológico de Monterrey|Anáhuac|ITAM|UDLAP|Iberoamericana|UNAM|IPN|UVM|UNITEC|Aliat)\b",
        r"\b(universidad|escuela|colegio|educación|edtech)\b",
    ],
    "Consumo": [
        r"\b(consumo|consumidor|ANTAD|FMI|gasto en|venta minorista)\b",
    ],
}

# ========================================================================
# TAXONOMÍA — Tipos de evento comercial
# ========================================================================
EVENTOS = {
    "M&A · Adquisición": [
        r"\b(adquir[ií]|adquisic|adquiri|adquir.|fusi[oó]n|comprar?[áó]?|compra|OPA|takeover|joint venture|JV)\b",
        r"\b(M&A|merger|acquisition|consolidación)\b",
    ],
    "Inversión / Capex": [
        r"\b(invertir|inversión|inversor|inversionista|capex|capacidad instalada|expansión|ampliación)\b",
        r"\b(nueva planta|nuevo centro|nuevo complejo|nueva fábrica|nuevo centro de distribución)\b",
        r"\b(millones? de dólares|millones? de pesos|MDD|MDP|inyectará|destinará|construirá)\b",
    ],
    "Resultados Financieros": [
        r"\b(resultados (?:trimestrales?|anuales|del|de))\b",
        r"\b(reporte trimestral|earnings|EBITDA|utilidad|ingresos|ventas netas|margen|flujo de efectivo)\b",
        r"\b(primer trimestre|segundo trimestre|tercer trimestre|cuarto trimestre|1T|2T|3T|4T|1Q|2Q|3Q|4Q|TTM)\b",
    ],
    "Movimientos Directivos": [
        r"\b(nombramient|designación|nuevo director|nuevo CEO|nuevo CFO|nuevo COO|nuevo presidente)\b",
        r"\b(asume|asumirá|asumió|toma las riendas|releva|sustituirá|sustituye|renuncia|dimisión|sale de|deja el cargo)\b",
        r"\b(consejo de administración|board|consejero independiente)\b",
    ],
    "Salida a Bolsa / IPO": [
        r"\b(IPO|salida a bolsa|oferta pública inicial|debut bursátil|debut en la bolsa)\b",
        r"\b(listará|listarse|colocación|emisión|tap issue)\b",
    ],
    "Rondas de Capital": [
        r"\b(ronda (?:de )?(?:capital|funding|inversión|Serie [A-D]))\b",
        r"\b(Series? [A-D]|capital semilla|seed round|venture)\b",
        r"\b(levantó|cerró ronda|recibió inversión)\b",
    ],
    "Expansión / Apertura": [
        r"\b(abrir|abrirá|abrió|inaugur|expand|llega a|aterriza en|debuta en)\b",
        r"\b(nuevas tiendas|nueva sucursal|nuevas sucursales|nuevo restaurante|nuevos restaurantes)\b",
        r"\b(franquicia|presencia en|operaciones en)\b",
    ],
    "Sucesión Familiar": [
        r"\b(sucesión|next-?gen|generación|hijo|heredero|familia|family office|profesionalización)\b",
    ],
    "Regulación / Política": [
        r"\b(COFECE|CNBV|CRE|CNH|IFETEL|IFT|PROFECO|CONDUSEF|SAT|SE|Banxico|Hacienda|SHCP|SEMARNAT|CONAGUA)\b",
        r"\b(regulación|reforma|ley general|decreto|nueva ley|prohibición|impuesto)\b",
    ],
    "Crisis / Reestructura": [
        r"\b(quiebra|insolvencia|reestructura|concurso mercantil|chapter 11|despidos)\b",
        r"\b(crisis|escándalo|investigación|demanda|fraude)\b",
    ],
    "Internacional": [
        r"\b(Estados Unidos|EUA|EEUU|EU |T-?MEC|nearshoring|aranceles|relocalización|exportación|tariff)\b",
        r"\b(Trump|Sheinbaum|Biden|Casa Blanca|US Trade|USMCA)\b",
    ],
}

# ========================================================================
# EMPRESAS / FAMILIAS AAA+AA del CRM LCG (extracto del PPT)
# ========================================================================
EMPRESAS_AAA = {
    # Veracruz
    "Chedraui": "Veracruz",
    "Café Parroquia": "Veracruz",
    "GOMSA": "Veracruz",
    "GRUVER": "Veracruz",
    "Unión Veracruzana": "Veracruz",
    "Citibanamex": "Veracruz",
    "Banamex": "Veracruz",
    "Acero HESA": "Veracruz",
    # Yucatán
    "Bepensa": "Yucatán",
    "Galletas Dondé": "Yucatán",
    "Dunosusa": "Yucatán",
    # Puebla
    "La Italiana": "Puebla",
    "La Morena": "Puebla",
    "El Calvario": "Puebla",
    "PATSA": "Puebla",
    # Quintana Roo
    "The Palace Company": "Quintana Roo",
    "Palace Resorts": "Quintana Roo",
    "Xcaret": "Quintana Roo",
    "Experiencias Xcaret": "Quintana Roo",
    "Original Resorts": "Quintana Roo",
    # Tabasco
    "Grupo Cruces": "Tabasco",
    "Chocolates Wolter": "Tabasco",
    "Grupo CICAS": "Tabasco",
    # Hidalgo
    "Grupo Autofin": "Hidalgo",
    "Autofin": "Hidalgo",
    "Corporativo UNNE": "Hidalgo",
    "TENPAC": "Hidalgo",
    # Chiapas
    "Grupo Farrera": "Chiapas",
    "Finca Hamburgo": "Chiapas",
    "Chiripa": "Chiapas",
    # Guerrero
    "Mundo Imperial": "Guerrero",
    "Grupo Hermes": "Guerrero",
    "Vidanta": "Guerrero",
    "Grupo Vidanta": "Guerrero",
    "Superfarmacias Leyva": "Guerrero",
    # Oaxaca
    "Casa Cortés": "Oaxaca",
    "Casa Cortés Mezcal": "Oaxaca",
    "Hospital San José Oaxaca": "Oaxaca",
    # Campeche
    "Grupo Richaud": "Campeche",
    "Richaud Hnos": "Campeche",
}

# ========================================================================
# CARGA + TAG
# ========================================================================

def load_posts() -> list[dict]:
    files = sorted(POSTS_DIR.glob("*.json"))
    posts = []
    for f in files:
        try:
            posts.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    posts.sort(key=lambda p: p.get("post_date", ""), reverse=True)
    return posts


def match_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE | re.UNICODE) for p in patterns)


def find_matches(text: str, taxonomy: dict[str, list[str]]) -> list[str]:
    """Devuelve las categorías cuyos patrones aparecen en el texto."""
    found = []
    for cat, patterns in taxonomy.items():
        if match_any(text, patterns):
            found.append(cat)
    return found


def find_companies(text: str) -> list[tuple[str, str]]:
    """Devuelve lista de (empresa, estado) detectadas."""
    found = []
    for empresa, estado in EMPRESAS_AAA.items():
        if re.search(r"\b" + re.escape(empresa) + r"\b", text, flags=re.IGNORECASE):
            found.append((empresa, estado))
    return found


def tag_post(post: dict) -> dict:
    """Añade tags al post: states, sectors, events, companies."""
    body = post.get("body_md") or ""
    subtitle = post.get("subtitle") or ""
    title = post.get("title") or ""
    full_text = f"{title}\n{subtitle}\n{body}"

    states = find_matches(full_text, ESTADOS_PATTERNS)
    sectors = find_matches(full_text, SECTORES)
    events = find_matches(full_text, EVENTOS)
    companies = find_companies(full_text)

    return {
        **post,
        "tags": {
            "states": states,
            "states_zona": [s for s in states if s in ZONA_ESTADOS],
            "sectors": sectors,
            "events": events,
            "companies_aaa": [{"name": c, "state": s} for c, s in companies],
        }
    }


# ========================================================================
# HTML rendering — comparte CSS con render_brief
# ========================================================================

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Manrope:wght@400;500;600;700&display=swap');
:root {
    --lcg-dark:#085E54; --lcg-green:#03B585; --lcg-mint:#8AF4E9;
    --lcg-cream:#F2EEE8; --lcg-ink:#1A1E1B; --lcg-ink-60:rgba(26,30,27,0.62);
    --lcg-line:rgba(8,94,84,0.18);
}
* { box-sizing: border-box; }
html, body { margin:0; padding:0; background:var(--lcg-cream); color:var(--lcg-ink); font-family:'Manrope',sans-serif; font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased; }
.frame { padding: 64px 80px; max-width: 1400px; margin: 0 auto; }
.chrome-top, .chrome-bottom { display:flex; justify-content:space-between; padding: 24px 80px; font-size:11px; font-weight:600; letter-spacing:0.22em; text-transform:uppercase; color:var(--lcg-ink-60); border-bottom: 1px solid var(--lcg-line); }
.chrome-bottom { border-bottom:none; border-top:1px solid var(--lcg-line); margin-top: 64px; }
.emblem { display:inline-block; width:8px; height:8px; background:var(--lcg-green); border-radius:999px; margin-left:10px; vertical-align: middle; }

h1, h2, h3, h4 { font-family:'Fraunces', serif; font-weight: 300; letter-spacing: -0.03em; line-height: 1.02; margin: 0; }
h1.hero { font-weight:200; font-size: clamp(56px, 8vw, 112px); margin-bottom: 12px; }
h2.section { font-weight:300; font-size: clamp(40px, 5vw, 72px); margin: 80px 0 16px 0; padding-top: 32px; border-top: 1px solid var(--lcg-line); }
h2.section:first-of-type { border-top: none; padding-top: 0; margin-top: 32px; }
h3 { font-size: 28px; margin: 24px 0 8px 0; color: var(--lcg-dark); }
em { font-style: italic; color: var(--lcg-green); }
.eyebrow { font-family:'Manrope', sans-serif; font-size:12px; font-weight:600; letter-spacing:0.24em; text-transform: uppercase; color: var(--lcg-green); margin-bottom: 16px; display:inline-block; }
.meta { font-family:'Manrope', sans-serif; font-size:13px; font-weight:500; letter-spacing:0.16em; text-transform: uppercase; color: var(--lcg-ink-60); }

/* Stats grid */
.stats { display:grid; grid-template-columns: repeat(4, 1fr); gap: 32px; margin: 32px 0 48px 0; padding: 24px 0; border-top: 1px solid var(--lcg-line); border-bottom: 1px solid var(--lcg-line); }
.stat .num { font-family:'Fraunces', serif; font-weight: 200; font-size: 56px; line-height: 1; color: var(--lcg-dark); display:block; }
.stat .label { display:block; font-size:11px; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color: var(--lcg-ink-60); margin-top: 6px; }

/* Category card */
.cat-grid { display: grid; grid-template-columns: 1fr; gap: 0; }
.cat { padding: 28px 0; border-bottom: 1px solid var(--lcg-line); }
.cat-head { display: grid; grid-template-columns: 440px 1fr auto; gap: 32px; align-items: baseline; margin-bottom: 16px; }
.cat-head h3 { margin: 0; }
.cat-head .count { font-family:'Fraunces', serif; font-weight: 200; font-size: 48px; line-height: 1; color: var(--lcg-green); }

/* Post list */
.post-list { list-style: none; padding: 0; margin: 0; }
.post-list li { padding: 14px 0; border-top: 1px solid var(--lcg-line); display: grid; grid-template-columns: 110px 1fr auto; gap: 24px; align-items: baseline; }
.post-list li:first-child { border-top: none; }
.post-list .date { font-family:'Fraunces', serif; font-weight: 300; font-size: 15px; color: var(--lcg-dark); }
.post-list .topic { font-family:'Manrope', sans-serif; font-size: 14px; color: var(--lcg-ink); line-height: 1.5; }
.post-list .topic a { color: inherit; text-decoration: none; border-bottom: 1px dashed var(--lcg-line); }
.post-list .topic a:hover { border-bottom-color: var(--lcg-green); color: var(--lcg-dark); }
.post-list .tags { font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--lcg-ink-60); white-space: nowrap; }
.post-list .tags span { display: inline-block; padding: 2px 8px; border: 1px solid var(--lcg-line); border-radius: 999px; margin-left: 4px; }

/* State block */
.state { padding: 48px 0; border-top: 2px solid var(--lcg-dark); }
.state:first-of-type { border-top: none; }
.state-head { display: grid; grid-template-columns: 440px 1fr; gap: 48px; align-items: end; margin-bottom: 32px; }
.state-head h2 { margin: 0; font-size: 64px; font-weight: 200; }
.state-head .stats-mini { display: flex; gap: 32px; }
.state-head .stats-mini .stat-mini .v { font-family:'Fraunces', serif; font-weight: 300; font-size: 32px; line-height: 1; color: var(--lcg-dark); }
.state-head .stats-mini .stat-mini .l { font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-ink-60); margin-top: 4px; display: block; }

/* TOC nav */
.toc { display: flex; flex-wrap: wrap; gap: 8px; margin: 24px 0 48px 0; padding: 16px 0; border-top: 1px solid var(--lcg-line); border-bottom: 1px solid var(--lcg-line); }
.toc a { font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 6px 14px; border: 1px solid var(--lcg-line); border-radius: 999px; color: var(--lcg-dark); text-decoration: none; }
.toc a:hover { background: var(--lcg-green); color: var(--lcg-cream); border-color: var(--lcg-green); }

/* Sector tag pills inside state */
.sector-pills { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 24px 0; }
.sector-pills span { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; padding: 4px 12px; border-radius: 999px; background: rgba(3,181,133,0.1); color: var(--lcg-dark); }
.sector-pills .count { font-weight: 400; color: var(--lcg-ink-60); margin-left: 6px; }

/* Company callouts */
.companies { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 24px 0 32px 0; }
.company { padding: 14px 18px; border: 1px solid var(--lcg-line); border-radius: 2px; }
.company .name { font-family: 'Fraunces', serif; font-weight: 400; font-size: 18px; color: var(--lcg-dark); }
.company .mentions { display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--lcg-green); margin-top: 4px; }

/* Footer */
footer { padding: 48px 80px; border-top: 1px solid var(--lcg-line); font-size: 12px; color: var(--lcg-ink-60); letter-spacing: 0.1em; }
footer em { color: var(--lcg-dark); }
"""


def chrome(label: str, breadcrumb: str) -> tuple[str, str]:
    top = f'<div class="chrome-top"><span>{html.escape(label)}<span class="emblem"></span></span><span>LCG · WHITEPAPER INTELLIGENCE</span></div>'
    bot = f'<div class="chrome-bottom"><span>{html.escape(breadcrumb)}</span><span>Generado · Mayo 2026</span></div>'
    return top, bot


def post_li(p: dict, show_tags: list[str] = None) -> str:
    """Renderiza un <li> con date · subtitle · tags pills."""
    topic = html.escape((p.get("subtitle") or "").strip() or p.get("title", ""))
    date = html.escape(p.get("date", ""))
    url = html.escape(p.get("url", ""))
    tags_html = ""
    if show_tags:
        pills = " ".join(f"<span>{html.escape(t)}</span>" for t in show_tags[:3])
        tags_html = f'<span class="tags">{pills}</span>'
    return f'<li><span class="date">{date}</span><span class="topic"><a href="{url}" target="_blank">{topic}</a></span>{tags_html}</li>'


# ========================================================================
# RENDER · CATEGORÍAS
# ========================================================================

def render_categorias_html(posts: list[dict]) -> str:
    by_sector = defaultdict(list)
    by_event = defaultdict(list)
    for p in posts:
        for s in p["tags"]["sectors"]:
            by_sector[s].append(p)
        for e in p["tags"]["events"]:
            by_event[e].append(p)

    total = len(posts)
    n_sectors = len(by_sector)
    n_events = len(by_event)
    total_tagged = sum(1 for p in posts if p["tags"]["sectors"] or p["tags"]["events"])

    top, bot = chrome("INTELIGENCIA POR CATEGORÍA", "BRIEF COMERCIAL · TAG: HOY · 247 POSTS")

    # TOC
    toc_sectors = " ".join(f'<a href="#sec-{html.escape(s.replace(" ","-").replace("/","").lower())}">{html.escape(s)} <em>{len(by_sector[s])}</em></a>' for s in sorted(by_sector, key=lambda k: -len(by_sector[k])))
    toc_events = " ".join(f'<a href="#ev-{html.escape(e.replace(" ","-").replace("/","").replace("·","").lower())}">{html.escape(e)} <em>{len(by_event[e])}</em></a>' for e in sorted(by_event, key=lambda k: -len(by_event[k])))

    # Sectors
    sec_html = []
    for s in sorted(by_sector, key=lambda k: -len(by_sector[k])):
        slug = s.replace(" ","-").replace("/","").lower()
        items = sorted(by_sector[s], key=lambda p: p.get("post_date",""), reverse=True)
        lis = "".join(post_li(p, p["tags"]["events"]) for p in items)
        sec_html.append(f"""
<div class="cat" id="sec-{html.escape(slug)}">
    <div class="cat-head">
        <h3>{html.escape(s)}</h3>
        <div></div>
        <span class="count">{len(items):03d}</span>
    </div>
    <ul class="post-list">{lis}</ul>
</div>""")

    # Events
    ev_html = []
    for e in sorted(by_event, key=lambda k: -len(by_event[k])):
        slug = e.replace(" ","-").replace("/","").replace("·","").lower()
        items = sorted(by_event[e], key=lambda p: p.get("post_date",""), reverse=True)
        lis = "".join(post_li(p, p["tags"]["sectors"]) for p in items)
        ev_html.append(f"""
<div class="cat" id="ev-{html.escape(slug)}">
    <div class="cat-head">
        <h3>{html.escape(e)}</h3>
        <div></div>
        <span class="count">{len(items):03d}</span>
    </div>
    <ul class="post-list">{lis}</ul>
</div>""")

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>Inteligencia Comercial · Por Categoría · LCG</title>
<style>{CSS}</style></head><body>
{top}
<main class="frame">
    <span class="eyebrow">INTELIGENCIA COMERCIAL · LCG</span>
    <h1 class="hero">Inteligencia <em>por categoría</em>.</h1>
    <p class="meta">Categorización automática de 247 posts del tag «hoy» de Whitepaper.mx · Mayo 2025 — Mayo 2026</p>

    <div class="stats">
        <div class="stat"><span class="num">{total}</span><span class="label">Posts totales</span></div>
        <div class="stat"><span class="num">{total_tagged}</span><span class="label">Posts taggeados</span></div>
        <div class="stat"><span class="num">{n_sectors}</span><span class="label">Sectores</span></div>
        <div class="stat"><span class="num">{n_events}</span><span class="label">Tipos de evento</span></div>
    </div>

    <h2 class="section">Sectores</h2>
    <div class="toc">{toc_sectors}</div>
    <div class="cat-grid">{''.join(sec_html)}</div>

    <h2 class="section">Tipos de evento</h2>
    <div class="toc">{toc_events}</div>
    <div class="cat-grid">{''.join(ev_html)}</div>
</main>
<footer>LCG · Whitepaper Intelligence · Compilado automatizado · Cookie expira: la del operador · Las opiniones del medio son de Whitepaper.mx, no de LCG.</footer>
{bot}
</body></html>"""


def render_categorias_txt(posts: list[dict]) -> str:
    by_sector = defaultdict(list)
    by_event = defaultdict(list)
    for p in posts:
        for s in p["tags"]["sectors"]:
            by_sector[s].append(p)
        for e in p["tags"]["events"]:
            by_event[e].append(p)

    out = []
    hr = lambda c="=", w=80: c * w
    out.append(hr("="))
    out.append("LCG · WHITEPAPER INTELLIGENCE · INTELIGENCIA POR CATEGORÍA")
    out.append(hr("="))
    out.append("")
    out.append(f"  Posts totales:    {len(posts)}")
    out.append(f"  Sectores:         {len(by_sector)}")
    out.append(f"  Tipos de evento:  {len(by_event)}")
    out.append("")

    out.append(hr("="))
    out.append("SECTORES (ordenados por frecuencia)")
    out.append(hr("="))
    out.append("")
    for s in sorted(by_sector, key=lambda k: -len(by_sector[k])):
        items = sorted(by_sector[s], key=lambda p: p.get("post_date",""), reverse=True)
        out.append(f"## {s.upper()}  ({len(items)} posts)")
        out.append(hr("-"))
        for p in items:
            topic = (p.get("subtitle") or p.get("title") or "")[:70]
            out.append(f"  {p.get('date',''):<12} {topic}")
        out.append("")

    out.append(hr("="))
    out.append("TIPOS DE EVENTO (ordenados por frecuencia)")
    out.append(hr("="))
    out.append("")
    for e in sorted(by_event, key=lambda k: -len(by_event[k])):
        items = sorted(by_event[e], key=lambda p: p.get("post_date",""), reverse=True)
        out.append(f"## {e.upper()}  ({len(items)} posts)")
        out.append(hr("-"))
        for p in items:
            topic = (p.get("subtitle") or p.get("title") or "")[:70]
            out.append(f"  {p.get('date',''):<12} {topic}")
        out.append("")
    return "\n".join(out)


# ========================================================================
# RENDER · ZONA (11 estados Sur-Centro-Golfo)
# ========================================================================

def render_zona_html(posts: list[dict]) -> str:
    # Filtramos: posts que mencionan al menos uno de los 11 estados
    zone_posts = [p for p in posts if p["tags"]["states_zona"]]

    # Por estado: posts, conteos sectoriales, empresas mencionadas
    by_state = defaultdict(list)
    for p in posts:
        for st in p["tags"]["states_zona"]:
            by_state[st].append(p)

    # Order de estados: por CRM weight (del PPT)
    state_order = ["Puebla", "Quintana Roo", "Veracruz", "Yucatán", "Hidalgo",
                   "Campeche", "Tabasco", "Guerrero", "Chiapas", "Oaxaca"]

    crm_data = {
        "Puebla":       (69, 148, "Automotriz · alimentos · retail"),
        "Quintana Roo": (56, 124, "Turismo · hospitalidad"),
        "Veracruz":     (46, 98,  "Puerto · petroquímica · agroindustria"),
        "Yucatán":      (34, 89,  "Bebidas (Bepensa) · retail · turismo"),
        "Hidalgo":      (14, 34,  "Calzado · automotriz · retail"),
        "Campeche":     (10, 19,  "Apícola · pesquero · alimentos"),
        "Tabasco":      (8,  15,  "Cacao · automotriz"),
        "Guerrero":     (7,  14,  "Turismo (Mundo Imperial · Vidanta)"),
        "Chiapas":      (5,  7,   "Café Soconusco · automotriz · hoteles"),
        "Oaxaca":       (4,  6,   "Mezcal · café Pluma Hidalgo"),
    }

    top, bot = chrome("ZONA SUR-CENTRO-GOLFO", "11 ESTADOS · DEEP DIVE COMERCIAL")

    # TOC
    toc = " ".join(f'<a href="#st-{st.lower().replace(" ","-")}">{html.escape(st)} <em>{len(by_state[st])}</em></a>' for st in state_order)

    state_blocks = []
    for st in state_order:
        st_posts = by_state.get(st, [])
        if not st_posts:
            continue
        st_slug = st.lower().replace(" ", "-")
        aaa, dm, industrias = crm_data.get(st, (0, 0, ""))

        # Top sectores
        sector_count = Counter()
        for p in st_posts:
            for s in p["tags"]["sectors"]:
                sector_count[s] += 1
        sector_pills = "".join(
            f'<span>{html.escape(s)}<span class="count">{n}</span></span>'
            for s, n in sector_count.most_common(8)
        )

        # Empresas AAA mencionadas en posts de este estado
        company_count = Counter()
        for p in st_posts:
            for c in p["tags"]["companies_aaa"]:
                if c["state"] == st:
                    company_count[c["name"]] += 1
        companies_html = ""
        if company_count:
            cards = "".join(
                f'<div class="company"><span class="name">{html.escape(c)}</span><span class="mentions">{n} mención{"es" if n>1 else ""}</span></div>'
                for c, n in company_count.most_common(12)
            )
            companies_html = f'<h3>Empresas/familias del CRM mencionadas</h3><div class="companies">{cards}</div>'

        # Lista de posts del estado
        items = sorted(st_posts, key=lambda p: p.get("post_date",""), reverse=True)
        lis = "".join(post_li(p, p["tags"]["sectors"][:2] + p["tags"]["events"][:1]) for p in items)

        state_blocks.append(f"""
<section class="state" id="st-{st_slug}">
    <div class="state-head">
        <div>
            <span class="eyebrow">Estado · {len(st_posts)} menciones en posts</span>
            <h2>{html.escape(st)}</h2>
            <p class="meta">{html.escape(industrias)}</p>
        </div>
        <div class="stats-mini">
            <div class="stat-mini"><span class="v">{aaa}</span><span class="l">AAA+AA CRM</span></div>
            <div class="stat-mini"><span class="v">{dm}</span><span class="l">Decision makers</span></div>
            <div class="stat-mini"><span class="v">{len(st_posts)}</span><span class="l">Notas comerciales</span></div>
        </div>
    </div>

    <h3>Sectores más mencionados</h3>
    <div class="sector-pills">{sector_pills}</div>

    {companies_html}

    <h3>Notas comerciales (orden cronológico inverso)</h3>
    <ul class="post-list">{lis}</ul>
</section>""")

    n_total = len(zone_posts)
    n_universo = len(posts)
    pct = (n_total / n_universo * 100) if n_universo else 0

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>Zona Sur-Centro-Golfo · Deep Dive Comercial · LCG</title>
<style>{CSS}</style></head><body>
{top}
<main class="frame">
    <span class="eyebrow">INICIATIVA COMERCIAL · LCG</span>
    <h1 class="hero">Zona <em>Sur-Centro-Golfo</em>.</h1>
    <p class="meta">Inteligencia comercial sobre los 11 estados · 294 AAA+AA · 650 decision makers · 62 familias mapeadas</p>

    <div class="stats">
        <div class="stat"><span class="num">11</span><span class="label">Estados</span></div>
        <div class="stat"><span class="num">{n_total}</span><span class="label">Posts con menciones</span></div>
        <div class="stat"><span class="num">{pct:.0f}%</span><span class="label">Del universo total</span></div>
        <div class="stat"><span class="num">{n_universo}</span><span class="label">Posts universo</span></div>
    </div>

    <div class="toc">{toc}</div>

    {''.join(state_blocks)}
</main>
<footer>LCG · Iniciativa Comercial Sur-Centro-Golfo · Mayo 2026 · Coordina FRAY (Dir. Ops.) · Fuente: Whitepaper.mx (suscripción pagada · uso interno).</footer>
{bot}
</body></html>"""


def render_zona_txt(posts: list[dict]) -> str:
    by_state = defaultdict(list)
    for p in posts:
        for st in p["tags"]["states_zona"]:
            by_state[st].append(p)
    state_order = ["Puebla", "Quintana Roo", "Veracruz", "Yucatán", "Hidalgo",
                   "Campeche", "Tabasco", "Guerrero", "Chiapas", "Oaxaca"]
    hr = lambda c="=", w=80: c * w
    out = []
    out.append(hr("="))
    out.append("LCG · ZONA SUR-CENTRO-GOLFO · DEEP DIVE COMERCIAL")
    out.append(hr("="))
    out.append("")
    for st in state_order:
        if not by_state.get(st):
            continue
        items = sorted(by_state[st], key=lambda p: p.get("post_date",""), reverse=True)
        sector_count = Counter(s for p in items for s in p["tags"]["sectors"])
        company_count = Counter(c["name"] for p in items for c in p["tags"]["companies_aaa"] if c["state"] == st)
        out.append(hr("="))
        out.append(f"  {st.upper()}  ·  {len(items)} notas comerciales")
        out.append(hr("="))
        if sector_count:
            out.append("")
            out.append("  Sectores más mencionados:")
            for s, n in sector_count.most_common(6):
                out.append(f"    · {s} ({n})")
        if company_count:
            out.append("")
            out.append("  Empresas/familias AAA mencionadas:")
            for c, n in company_count.most_common(8):
                out.append(f"    · {c} ({n} menciones)")
        out.append("")
        out.append("  NOTAS COMERCIALES:")
        out.append(hr("-"))
        for p in items:
            topic = (p.get("subtitle") or p.get("title") or "")[:70]
            sectors = ", ".join(p["tags"]["sectors"][:2]) or "-"
            out.append(f"  {p.get('date',''):<12} {topic[:60]:<60} [{sectors[:20]}]")
        out.append("")
        out.append("")
    return "\n".join(out)


# ========================================================================
# MAIN
# ========================================================================

def main():
    print("="*72)
    print("ANALYZE — Inteligencia comercial LCG sobre Whitepaper")
    print("="*72)

    posts = load_posts()
    if not posts:
        print(f"ERROR: no encontré posts en {POSTS_DIR}")
        return
    print(f"  Cargados: {len(posts)} posts")

    print("  Categorizando...", end=" ")
    tagged = [tag_post(p) for p in posts]
    print("✓")

    # Stats
    n_tagged = sum(1 for p in tagged if p["tags"]["sectors"] or p["tags"]["events"])
    n_zone = sum(1 for p in tagged if p["tags"]["states_zona"])
    sectors = Counter(s for p in tagged for s in p["tags"]["sectors"])
    events = Counter(e for p in tagged for e in p["tags"]["events"])
    print(f"  · {n_tagged} con sector o evento taggeado")
    print(f"  · {n_zone} con mención de la zona Sur-Centro-Golfo")
    print(f"  · Top 5 sectores: {[s for s,_ in sectors.most_common(5)]}")
    print(f"  · Top 5 eventos: {[e for e,_ in events.most_common(5)]}")

    # Save tagged index (without body to keep size manageable)
    tagged_light = [{**p, "body_html": None, "body_md": None} for p in tagged]
    (OUT / "tagged_index.json").write_text(json.dumps(tagged_light, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"  ✓ tagged_index.json")

    # Render
    (OUT / "categorias.html").write_text(render_categorias_html(tagged), encoding="utf-8")
    (OUT / "categorias.txt").write_text(render_categorias_txt(tagged), encoding="utf-8")
    print(f"  ✓ categorias.html / .txt")

    (OUT / "zona.html").write_text(render_zona_html(tagged), encoding="utf-8")
    (OUT / "zona.txt").write_text(render_zona_txt(tagged), encoding="utf-8")
    print(f"  ✓ zona.html / .txt")

    print("="*72)
    print("LISTO")


if __name__ == "__main__":
    main()
