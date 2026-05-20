#!/usr/bin/env python3
"""
========================================================================
STATE INTELLIGENCE v2 — Inteligencia comercial por estado
========================================================================
Para cada uno de los 11 estados de la zona Sur-Centro-Golfo produce un
HTML con inteligencia comercial REAL extraída de los posts de Whitepaper:

  - Tendencias recientes (top sectores, top eventos)
  - Familias del PPT (CRM AAA+AA) mencionadas con extractos
  - NUEVAS referencias detectadas (empresas no listadas en PPT)
  - Extractos textuales del body con la noticia exacta
  - Timeline de menciones

Outputs:
    docs/estado-puebla.html · docs/estado-veracruz.html · etc.
    docs/zona.html (overview de los 11 estados)
    docs/index.html (menú principal)
    docs/brief.html, docs/categorias.html (copiados desde output/)
    docs/styles.css (compartido)
========================================================================
"""

import json
import re
import html
import shutil
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

OUT = Path("./output")
POSTS_DIR = OUT / "posts"
DOCS = Path("./docs")

# ========================================================================
# TAXONOMÍA — Estados zona + ciudades
# ========================================================================
ZONA_ESTADOS = ["Puebla", "Quintana Roo", "Veracruz", "Tamaulipas", "Yucatán", "Hidalgo",
                "Campeche", "Tabasco", "Guerrero", "Chiapas", "Oaxaca"]

# Patrones por estado: nombre + ciudades clave
ESTADOS_PATTERNS = {
    "Puebla":       [r"\bPuebla\b", r"\bCholula\b", r"\bTehuacán\b"],
    "Quintana Roo": [r"\bQuintana Roo\b", r"\bCancún\b", r"\bPlaya del Carmen\b",
                     r"\bRiviera Maya\b", r"\bTulum\b", r"\bChetumal\b", r"\bIsla Mujeres\b"],
    "Veracruz":     [r"\bVeracruz\b", r"\bXalapa\b", r"\bCoatzacoalcos\b", r"\bTuxpan\b",
                     r"\bMinatitlán\b", r"\bCórdoba(?!\s+de\s+)\b", r"\bOrizaba\b",
                     r"\bPoza Rica\b", r"\bCoatepec\b", r"\bPapantla\b"],
    "Tamaulipas":   [r"\bTamaulipas\b", r"\bTampico\b", r"\bReynosa\b", r"\bMatamoros\b",
                     r"\bNuevo Laredo\b", r"\bAltamira\b", r"\bCiudad Victoria\b",
                     r"\bCiudad Madero\b", r"\bMadero\b"],
    "Yucatán":      [r"\bYucatán\b", r"\bMérida\b", r"\bValladolid\b", r"\bProgreso\b"],
    "Hidalgo":      [r"\bHidalgo\b", r"\bPachuca\b", r"\bTula\b", r"\bTulancingo\b"],
    "Campeche":     [r"\bCampeche\b", r"\bCalkiní\b", r"\bChampotón\b", r"\bHopelchén\b",
                     r"\bCiudad del Carmen\b"],
    "Tabasco":      [r"\bTabasco\b", r"\bVillahermosa\b"],
    "Guerrero":     [r"\bGuerrero\b", r"\bAcapulco\b", r"\bIxtapa\b", r"\bZihuatanejo\b",
                     r"\bTaxco\b", r"\bChilpancingo\b"],
    "Chiapas":      [r"\bChiapas\b", r"\bTuxtla\b", r"\bSan Cristóbal\b", r"\bTapachula\b",
                     r"\bSoconusco\b"],
    "Oaxaca":       [r"\bOaxaca\b", r"\bHuatulco\b", r"\bPluma Hidalgo\b", r"\bSalina Cruz\b"],
}

# CRM data del PPT (por estado)
CRM_DATA = {
    "Puebla":       {"aaa_aa": 69, "dm": 148, "industries": "Automotriz · alimentos · retail"},
    "Quintana Roo": {"aaa_aa": 56, "dm": 124, "industries": "Turismo · hospitalidad"},
    "Veracruz":     {"aaa_aa": 46, "dm": 98,  "industries": "Puerto · petroquímica · agroindustria"},
    "Tamaulipas":   {"aaa_aa": 41, "dm": 96,  "industries": "Frontera Nuevo Laredo · puerto Altamira · maquila · agroindustria"},
    "Yucatán":      {"aaa_aa": 34, "dm": 89,  "industries": "Bebidas (Bepensa) · retail · turismo"},
    "Hidalgo":      {"aaa_aa": 14, "dm": 34,  "industries": "Calzado · automotriz · retail"},
    "Campeche":     {"aaa_aa": 10, "dm": 19,  "industries": "Apícola · pesquero · alimentos"},
    "Tabasco":      {"aaa_aa": 8,  "dm": 15,  "industries": "Cacao · automotriz"},
    "Guerrero":     {"aaa_aa": 7,  "dm": 14,  "industries": "Turismo (Mundo Imperial · Vidanta)"},
    "Chiapas":      {"aaa_aa": 5,  "dm": 7,   "industries": "Café Soconusco · automotriz · hoteles"},
    "Oaxaca":       {"aaa_aa": 4,  "dm": 6,   "industries": "Mezcal · café Pluma Hidalgo"},
}

# ========================================================================
# FAMILIAS / EMPRESAS AAA+AA del PPT (cross-reference)
# ========================================================================
PPT_FAMILIAS = {
    "Veracruz": [
        ("Chedraui",         ["Chedraui", "Chedraui Obeso"]),
        ("Hernández Ramírez", ["Hernández Ramírez", "Banamex Tuxpan", "ex-Citibanamex"]),
        ("Chahín Trueba",    ["Chahín Trueba", "Acero HESA", "Fletes HESA"]),
        ("Café Parroquia",   ["Café Parroquia", "Parroquia", "Vergara"]),
        ("GOMSA",            ["GOMSA", "Gómez Malpica"]),
        ("GRUVER",           ["GRUVER", "Ramón Gomez Gomez"]),
        ("Unión Veracruzana", ["Unión Veracruzana", "Exsome"]),
    ],
    "Tamaulipas": [
        ("Grossman (Arca Continental · USD 2.2B Forbes)", ["Grossman", "Arca Continental"]),
        ("González Díaz Lombardo (Tequila Chinaco · DO Tamaulipas)", ["González Díaz Lombardo", "Tequila Chinaco"]),
        ("Fleishman (Grupo Tampico · post-fusión KOF 2011)", ["Fleishman", "Grupo Tampico"]),
        ("Familia Osuna (Ciudad Victoria · Transpaís + Inbox + Car One)", ["Osuna", "Transpaís", "Car One"]),
        ("Cluster aduanal Nuevo Laredo (Pumarejo / Maron)", ["Pumarejo", "Maron", "Garza Quintero", "Lopezadri"]),
        ("Familia Vela (raíz Tampico · opera Quintana Roo)", ["familia Vela", "Vela Tampico"]),
        ("Estrada Ávalos", ["Estrada Ávalos"]),
    ],
    "Yucatán": [
        ("Bepensa (Ponce Díaz)", ["Bepensa", "Ponce Díaz", "Pepsi Bepensa"]),
        ("Galletas Dondé (Gómory)", ["Galletas Dondé", "Dondé", "Gómory"]),
        ("Dunosusa (Ricalde Durán)", ["Dunosusa", "Ricalde Durán"]),
    ],
    "Puebla": [
        ("La Italiana (Cernicchiaro)", ["La Italiana", "Cernicchiaro"]),
        ("La Morena (Ayala)",          ["La Morena", "Ayala"]),
        ("El Calvario / PATSA (Romero Bringas / Celis)", ["El Calvario", "PATSA", "Romero Bringas", "Celis"]),
    ],
    "Quintana Roo": [
        ("The Palace Company (Chapur Zahoul)", ["Palace Company", "Palace Resorts", "Chapur Zahoul", "Chapur"]),
        ("Experiencias Xcaret (Quintana Pali/Constandse)", ["Xcaret", "Quintana Pali", "Constandse", "Experiencias Xcaret"]),
        ("Original Resorts (De la Peña)", ["Original Resorts", "De la Peña"]),
    ],
    "Tabasco": [
        ("Grupo Cruces (automotriz)", ["Grupo Cruces"]),
        ("Chocolates Wolter (Wolter / Parizot Wolter)", ["Wolter", "Parizot Wolter", "Chocolates Wolter"]),
        ("Grupo CICAS (cacao + pimienta)", ["Grupo CICAS", "CICAS"]),
    ],
    "Hidalgo": [
        ("Grupo Autofin México (Hernández Venegas)", ["Autofin", "Hernández Venegas"]),
        ("Corporativo UNNE (Paredes)", ["Corporativo UNNE", "UNNE"]),
        ("TENPAC calzado (Márquez Ramírez)", ["TENPAC", "Márquez Ramírez"]),
    ],
    "Chiapas": [
        ("Grupo Farrera (Farrera Escudero)", ["Grupo Farrera", "Farrera Escudero"]),
        ("Finca Hamburgo (Edelmann Toriello)", ["Finca Hamburgo", "Edelmann Toriello", "Chiripa"]),
        ("Cluster cafetalero Soconusco", ["Soconusco", "Ruta del Café"]),
    ],
    "Guerrero": [
        ("Mundo Imperial / Grupo Hermes (Hank)", ["Mundo Imperial", "Grupo Hermes", "Hank"]),
        ("Grupo Vidanta (Chávez Madrazo)", ["Vidanta", "Chávez Madrazo"]),
        ("Superfarmacias Leyva", ["Superfarmacias Leyva", "Leyva"]),
    ],
    "Oaxaca": [
        ("Casa Cortés Mezcal", ["Casa Cortés", "Cortés Mezcal"]),
        ("Cluster cafetero Pluma Hidalgo + Sierra Sur", ["Pluma Hidalgo", "Sierra Sur"]),
        ("Instituto Sarmiento / Hospital San José", ["Instituto Sarmiento", "Hospital San José", "Sarmiento"]),
    ],
    "Campeche": [
        ("Grupo Richaud Hnos (alimentario)", ["Grupo Richaud", "Richaud Hnos", "Richaud"]),
        ("Azar Wabi (Turismo / liderazgo gremial)", ["Azar Wabi"]),
        ("Cluster apícola-pesquero", ["Calkiní", "Hopelchén", "Champotón"]),
    ],
}

# ========================================================================
# TAXONOMÍA SECTORES y EVENTOS (replicada de analyze.py, simplificada)
# ========================================================================
SECTORES = {
    "Alimentos y Bebidas": [r"\b(Coca[- ]Cola|Pepsi|Bimbo|Maseca|Gruma|La Costeña|Sigma|Lala|Alpura|Bachoco|Bepensa|Modelo|Heineken|Ab InBev|Constellation Brands)\b",
                           r"\b(refresco|cerveza|tequila|mezcal|cacao|chocolate|lácteo|panificadora|alimentos|bebida|alimentaria|gastronomía)\b"],
    "Retail / Comercio":   [r"\b(Chedraui|Soriana|Walmart|Costco|Liverpool|Suburbia|Palacio de Hierro|Sanborns|HEB|7-?Eleven|OXXO|Comercial Mexicana|Coppel|Elektra)\b",
                           r"\b(autoservicio|tienda departamental|cadena de tiendas|retail|e-?commerce|comercio electrónico|Mercado Libre)\b"],
    "Turismo / Hospitalidad": [r"\b(Vidanta|Xcaret|Palace|Posadas|RIU|Iberostar|Barceló|Marriott|Hilton|Hyatt|Fiesta Americana|Camino Real|Krystal|City Express)\b",
                              r"\b(turismo|hotel|hospedaje|resort|todo incluido|hospitalidad|Tianguis Turístico)\b"],
    "Automotriz": [r"\b(BMW|Audi|Ford|General Motors|GM|Stellantis|Nissan|Toyota|Honda|Mazda|Volkswagen|VW|Kia|Hyundai|Tesla|BYD|Chery|JAC|Geely|MG|Mercedes-?Benz)\b",
                  r"\b(ensambladora|autopartes|OEM|automotriz|ensamblaje|vehículo|EV|eléctric)\b"],
    "Banca / Finanzas": [r"\b(BBVA|Banamex|Citibanamex|Santander|Banorte|Inbursa|HSBC|Scotiabank|Banregio|Banco Azteca|Compartamos|Mifel|Multiva)\b",
                       r"\b(fintech|neobanco|Klar|Nu|Konfío|Stori)\b",
                       r"\b(seguros|aseguradora|GNP|MetLife|Mapfre|Quálitas)\b",
                       r"\b(crédito|préstamo|hipoteca|BMV|Bolsa Mexicana)\b"],
    "Energía / Petroquímica": [r"\b(Pemex|CFE|Iberdrola|Engie|Sempra|IEnova)\b",
                              r"\b(petroquímica|refinería|gas natural|hidrocarburo|gasolinera)\b",
                              r"\b(solar|eólico|renovable|fotovoltaic)\b"],
    "Real Estate / Construcción": [r"\b(Cemex|Holcim|Cementos Moctezuma|Cementos Cruz Azul|GCC|GCC Cementos)\b",
                                  r"\b(Fibra|FIBRA|Funo|Macquarie|Terrafina|Vinte|Javer)\b",
                                  r"\b(inmobiliari[ao]|construcción|vivienda|residencial)\b"],
    "Tecnología / Telecom": [r"\b(Telmex|Telcel|AT&T|Movistar|Megacable|Izzi|Totalplay)\b",
                            r"\b(Google|Microsoft|AWS|IBM|SAP|Oracle|Adobe|Salesforce)\b",
                            r"\b(startup|software|app móvil|SaaS|IA|inteligencia artificial)\b",
                            r"\b(Series [A-D]|ronda de capital|venture capital|VC|capital semilla|Kaszek|Mountain Nazca|Dalus|Wollef|Cometa)\b"],
    "Salud / Farma": [r"\b(Genomma|Pisa|Sanfer|Carnot|Liomont|Stendhal|Bayer|Pfizer|Roche|Sanofi|Merck|Lilly)\b",
                     r"\b(Farmacias del Ahorro|Farmacias Guadalajara|Farmacias Benavides|Farmacias San Pablo)\b",
                     r"\b(hospital|clínica|farmacéutic|laboratorio|biotecnología)\b"],
    "Agroindustria": [r"\b(agropecuario|agrícola|ganadero|cultivo|cosecha)\b",
                     r"\b(aguacate|café|cacao|agave|caña de azúcar|maíz|trigo|berry|frutícola|miel|apícola|pesca)\b"],
    "Logística / Transporte": [r"\b(DHL|FedEx|Estafeta|UPS|Redpack)\b",
                              r"\b(Aeroméxico|Volaris|Viva Aerobus|Magnicharters)\b",
                              r"\b(logística|transporte|fletes|paquetería|naviera|puerto|aeropuerto|Tren Maya|Tren Interurbano|ferroviario)\b"],
    "Manufactura / Nearshoring": [r"\b(manufactura|maquiladora|IMMEX|planta industrial|fábrica|nearshoring|relocalización|parque industrial)\b",
                                  r"\b(AHMSA|Ternium|ArcelorMittal|Deacero|Grupo México|Industrias Peñoles)\b",
                                  r"\b(siderurgia|acero|aluminio|cobre|minería)\b"],
    "Educación": [r"\b(Tec de Monterrey|ITESM|Anáhuac|ITAM|UDLAP|Iberoamericana|UNAM|IPN|UVM)\b",
                 r"\b(universidad|escuela|colegio|educación|edtech)\b"],
}

EVENTOS = {
    "M&A": [r"\b(adquir[ií]|adquisic|fusi[oó]n|comprar?[áó]?|compra de [A-Z]|OPA|takeover|joint venture)\b"],
    "Inversión / Capex": [r"\b(invertir[áé]|inversión|capex|nueva planta|nuevo centro|nueva fábrica|construirá|destinará|millones? de d[oó]lares|millones? de pesos|MDD|MDP|US\$|USD\s?\d)\b"],
    "Resultados": [r"\b(resultados (?:trimestrales?|anuales?|del primer|del segundo|del tercer|del cuarto)|reporte trimestral|EBITDA|utilidad neta|ingresos|ventas netas|primer trimestre|cuarto trimestre|1T|2T|3T|4T)\b"],
    "Movimientos directivos": [r"\b(nuevo (CEO|CFO|COO|director|presidente)|nombramiento|designación|asume|releva a|sustituirá|renuncia|dimisión|deja el cargo|consejo de administración)\b"],
    "IPO / Bursátil": [r"\b(IPO|salida a bolsa|debut bursátil|debut en la bolsa|listará|colocación primaria|emisión)\b"],
    "Funding / Rondas": [r"\b(ronda de (?:capital|inversión|Serie [A-D])|Series [A-D]|capital semilla|seed|levantó \$|cerró ronda)\b"],
    "Expansión / Apertura": [r"\b(abrir[áé]|inaugur|expand[ie]|aterriza en|debuta en|nueva sucursal|nuevas sucursales|nuevos restaurantes|franquicia|presencia en|operaciones en)\b"],
    "Familia / Sucesión": [r"\b(sucesión|next-?gen|generación|hijo|heredero|family office|profesionalización)\b"],
    "Regulación": [r"\b(COFECE|CNBV|CRE|CNH|IFETEL|IFT|PROFECO|CONDUSEF|SAT|Banxico|SHCP|SEMARNAT|CONAGUA|nueva ley|reforma|decreto|prohibición|impuesto a)\b"],
    "Crisis / Reestructura": [r"\b(quiebra|insolvencia|reestructura|concurso mercantil|chapter 11|despidos|cierre de planta)\b"],
}

# Stopwords para detección de entidades nuevas
ENTITY_STOPWORDS = {
    # geografías que no son familias
    "México", "Estados Unidos", "Estados Unido", "America Latina", "Latin America",
    "Casa Blanca", "Wall Street", "Silicon Valley", "Bay Area",
    "Banco Mundial", "Banco Central", "Fondo Monetario", "Naciones Unidas",
    "América Latina", "América del Norte", "América del Sur", "Centro América",
    "Norte América", "Sudamérica", "Cono Sur", "Costa Rica", "República Dominicana",
    "Puerto Rico", "El Salvador", "Hong Kong", "Sudáfrica", "Sri Lanka",
    "El Reino Unido", "Reino Unido", "Países Bajos", "Arabia Saudita", "Países Bajos",
    "El Caribe", "El Pacífico", "El Atlántico", "El Golfo", "El Norte", "El Sur",
    "El Centro", "El Bajío", "Río Bravo", "Río Grande",
    # tribunales / política
    "Tribunal Superior", "Tribunal Federal", "Tribunal Supremo", "Suprema Corte",
    "Tribunal Electoral", "Tribunal Constitucional",
    "Presidencia Municipal", "Presidencia Estatal", "Gobierno Federal",
    "Gobierno Estatal", "Cámara Baja", "Cámara Alta", "Senado",
    # estados mexicanos (no son familias)
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas",
    "Chihuahua", "Coahuila", "Colima", "Durango", "Estado de México", "Edomex",
    "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit",
    "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí",
    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas",
    "Ciudad de México", "Distrito Federal",
    # ciudades importantes
    "Monterrey", "Guadalajara", "Querétaro", "León", "Tijuana", "Mérida", "Cancún",
    "Hermosillo", "Saltillo", "Aguascalientes", "Mexicali",
    # comunes que no son negocios
    "Banca Pública", "Cuenta Pública", "Sector Público", "Sector Privado",
    "Mercado Mexicano", "Mercado Local", "Mercado Global",
    "Año Pasado", "Año Anterior", "Año Actual",
    "Cinco Minutos", "Whitepaper Hoy", "Whitepaper",
    "Comentario Whitepaper", "Comentario Editorial",
    # Sectores
    "Industria Automotriz", "Sector Energético",
    # Nombres genéricos
    "Ministerio Público", "Procuraduría Federal", "Procuraduría General",
    "El País", "El Mundo", "El Norte", "La Jornada", "Excélsior", "El Universal",
    "Wall Street Journal", "Financial Times", "New York Times", "Bloomberg",
}

# Sustantivos comunes que aparecen capitalizados al inicio de oración
SENTENCE_STARTERS = {
    "El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas",
    "Su", "Sus", "Mi", "Mis", "Tu", "Tus", "Nuestro", "Nuestra",
    "Este", "Esta", "Estos", "Estas", "Ese", "Esa", "Esos", "Esas",
    "Lo", "Le", "Les", "Se", "Me", "Te",
    "Y", "O", "Pero", "Aunque", "Mientras", "Cuando", "Donde",
    "Sin", "Con", "Por", "Para", "De", "Del", "En", "A", "Al",
    "Hoy", "Ayer", "Mañana", "Ahora", "Antes", "Después", "Luego",
}

# ========================================================================
# UTILIDADES
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


def split_topics(body_md: str) -> list[str]:
    """Divide el body en chunks por doble newline. Limita longitud."""
    chunks = re.split(r'\n{2,}', body_md.strip())
    out = []
    for c in chunks:
        c = c.strip()
        if 50 < len(c) < 2500:  # filtra muy corto (titulares sueltos) y muy largo (lista enorme)
            out.append(c)
    return out


def clean_excerpt(text: str) -> str:
    """Limpia un extracto: quita markdown bold/italic/links pero deja el texto."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # links → texto
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)            # bold
    t = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"\1", t) # italic
    t = re.sub(r"^#+\s+", "", t, flags=re.MULTILINE)    # heading markers
    t = re.sub(r"^\s*>\s+", "", t, flags=re.MULTILINE)  # blockquote
    t = re.sub(r"\s+", " ", t).strip()
    return t


def find_entities(text: str) -> list[str]:
    """
    Detecta posibles nombres de empresas/familias: secuencias de palabras
    capitalizadas (2-5 palabras) que no sean stopwords ni sentence-starters.
    """
    # Patrón: una o más palabras Capitalizadas, posiblemente unidas por "de", "y", "&"
    pattern = r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de\s+|del\s+|y\s+|&\s+|las?\s+|los?\s+)?[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,4})\b'
    matches = re.findall(pattern, text)
    out = []
    for m in matches:
        m = m.strip()
        words = m.split()
        # Filtra de 2-5 palabras (descarta single words)
        if not (2 <= len(words) <= 5):
            continue
        # Filtra si la primera palabra es sentence starter
        if words[0] in SENTENCE_STARTERS:
            # Si tiene 2+ palabras restantes que sí parecen entidad, recorta la primera
            if len(words) >= 3 and words[1][0].isupper():
                m = " ".join(words[1:])
                words = m.split()
            else:
                continue
        # Stopwords
        if m in ENTITY_STOPWORDS:
            continue
        # No queremos pura geografía
        if any(w in ENTITY_STOPWORDS for w in [m]):
            continue
        out.append(m)
    return out


def match_taxonomy(text: str, taxonomy: dict[str, list[str]]) -> list[str]:
    found = []
    for cat, patterns in taxonomy.items():
        if any(re.search(p, text, flags=re.IGNORECASE) for p in patterns):
            found.append(cat)
    return found


def find_ppt_families(text: str, state: str) -> list[tuple[str, str]]:
    """Para un texto, devuelve familias del PPT (matched_label, alias_que_apareció)."""
    found = []
    for label, aliases in PPT_FAMILIAS.get(state, []):
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", text, flags=re.IGNORECASE):
                found.append((label, alias))
                break  # uno por familia es suficiente
    return found


# ========================================================================
# CONSTRUCCIÓN DE INTELIGENCIA POR ESTADO
# ========================================================================

def build_state_intel(state: str, all_posts: list[dict]) -> dict:
    patterns = ESTADOS_PATTERNS[state]
    crm = CRM_DATA[state]

    # Compila todos los aliases de las familias PPT de este estado para usarlos
    # también como criterio de relevancia (post sobre Bepensa = relevante para Yucatán)
    family_aliases: list[str] = []
    for _label, aliases in PPT_FAMILIAS.get(state, []):
        family_aliases.extend(aliases)

    excerpts = []
    sector_count = Counter()
    event_count = Counter()
    family_mentions = defaultdict(list)
    entity_count = Counter()
    timeline = Counter()

    def topic_matches(topic: str) -> tuple[bool, str]:
        """Devuelve (relevante, motivo) — motivo es 'state' o 'family'."""
        if any(re.search(ptn, topic, re.IGNORECASE) for ptn in patterns):
            return True, "state"
        for alias in family_aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", topic, re.IGNORECASE):
                return True, "family"
        return False, ""

    for p in all_posts:
        body = p.get("body_md") or ""
        if not body:
            continue
        topics = split_topics(body)
        for tidx, topic in enumerate(topics):
            is_rel, reason = topic_matches(topic)
            if not is_rel:
                continue
            clean = clean_excerpt(topic)
            ex_idx = len(excerpts)
            excerpts.append({
                "date": p.get("date"),
                "post_date": p.get("post_date"),
                "url": p.get("url"),
                "subtitle": p.get("subtitle", "").strip(),
                "text": clean,
                "matched_by": reason,
            })
            # Sector/evento per excerpt
            for s in match_taxonomy(clean, SECTORES):
                sector_count[s] += 1
            for e in match_taxonomy(clean, EVENTOS):
                event_count[e] += 1
            # PPT family matches
            for label, alias in find_ppt_families(clean, state):
                family_mentions[label].append({
                    "date": p.get("date"),
                    "alias": alias,
                    "excerpt_idx": ex_idx,
                })
            # Entity detection (todas las capitalizadas)
            for e in find_entities(clean):
                entity_count[e] += 1
            # Timeline
            date_str = p.get("date", "")
            if len(date_str) >= 7:
                timeline[date_str[:7]] += 1

    # Sort excerpts desc by date
    excerpts.sort(key=lambda x: x.get("post_date", ""), reverse=True)
    # Re-map family_mentions excerpt_idx after sort
    # (Easier: track by post_date+text hash, but for now skip — recompute below)

    # Cleanup family_mentions — sort by date
    fm_clean = {}
    for label, mentions in family_mentions.items():
        # Dedupe by date
        seen = set()
        unique = []
        for m in mentions:
            if m["date"] not in seen:
                seen.add(m["date"])
                unique.append(m)
        unique.sort(key=lambda x: x["date"], reverse=True)
        fm_clean[label] = unique

    # Entidades nuevas: filtrar las que coinciden con familias PPT
    new_entities = []
    ppt_known_lower = set()
    for label, aliases in PPT_FAMILIAS.get(state, []):
        for a in aliases:
            ppt_known_lower.add(a.lower())
    for ent, n in entity_count.most_common(80):
        if n < 2:
            continue
        ent_lower = ent.lower()
        # Skip si contiene alias conocido
        if any(known in ent_lower or ent_lower in known for known in ppt_known_lower):
            continue
        # Skip estados / ciudades del propio estado
        if any(re.search(ptn, ent, re.IGNORECASE) for ptn in patterns):
            continue
        new_entities.append((ent, n))
        if len(new_entities) >= 25:
            break

    # Timeline ordenada
    months_sorted = sorted(timeline.keys())

    return {
        "state": state,
        "crm": crm,
        "total_excerpts": len(excerpts),
        "excerpts": excerpts,
        "top_sectors": sector_count.most_common(8),
        "top_events": event_count.most_common(8),
        "ppt_families_mentioned": fm_clean,
        "ppt_families_total": len(PPT_FAMILIAS.get(state, [])),
        "ppt_families_hit": len(fm_clean),
        "new_entities": new_entities,
        "timeline": [(m, timeline[m]) for m in months_sorted],
    }


# ========================================================================
# HTML RENDERING
# ========================================================================

def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[áä]", "a", s)
    s = re.sub(r"[éë]", "e", s)
    s = re.sub(r"[íï]", "i", s)
    s = re.sub(r"[óö]", "o", s)
    s = re.sub(r"[úü]", "u", s)
    s = re.sub(r"ñ", "n", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def chrome_header(active: str = "") -> str:
    """Header institucional con logo + nav."""
    links = [
        ("index.html",       "Inicio",      "inicio"),
        ("zona.html",        "Zona",        "zona"),
        ("categorias.html",  "Categorías",  "categorias"),
        ("brief.html",       "Brief",       "brief"),
    ]
    nav_html = "".join(
        f'<a href="{href}" class="{"active" if active == key else ""}">{html.escape(label)}</a>'
        for href, label, key in links
    )
    return f"""<header class="chrome">
    <a href="index.html" class="brand">
        <img src="assets/lcg-mark.svg" alt="LCG" class="mark">
        <div class="brand-text">
            <span class="brand-name">LCG</span>
            <span class="brand-tag">CONSULTING GROUP</span>
        </div>
    </a>
    <nav class="nav">{nav_html}</nav>
</header>"""


def chrome_footer() -> str:
    return f"""<footer class="chrome-foot">
    <span>LCG · Whitepaper Intelligence · Iniciativa Comercial Zona Sur-Centro-Golfo</span>
    <span>Mayo 2026 · 247 posts · Fuente: Whitepaper.mx (suscripción pagada · uso interno)</span>
</footer>"""


CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400&family=Manrope:wght@400;500;600;700&display=swap');

:root {
    --lcg-dark:#085E54; --lcg-green:#03B585; --lcg-mint:#8AF4E9;
    --lcg-cream:#F2EEE8; --lcg-ink:#1A1E1B; --lcg-ink-60:rgba(26,30,27,0.62);
    --lcg-line:rgba(8,94,84,0.18);
}
* { box-sizing: border-box; }
html, body { margin:0; padding:0; background:var(--lcg-cream); color:var(--lcg-ink); font-family:'Manrope',sans-serif; font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased; }
a { color: var(--lcg-dark); }

/* ====== Chrome header (sticky nav) ====== */
header.chrome { position: sticky; top: 0; z-index: 50; display: flex; align-items: center; justify-content: space-between;
                padding: 16px 48px; background: var(--lcg-cream); border-bottom: 1px solid var(--lcg-line); }
.brand { display: flex; align-items: center; gap: 14px; text-decoration: none; color: var(--lcg-dark); }
.brand .mark { width: 32px; height: 32px; }
.brand-text { display: flex; flex-direction: column; line-height: 1; }
.brand-name { font-family: 'Manrope', sans-serif; font-weight: 700; font-size: 16px; letter-spacing: 0.18em; color: var(--lcg-green); }
.brand-tag { font-family: 'Manrope', sans-serif; font-size: 9px; font-weight: 600; letter-spacing: 0.22em; color: var(--lcg-dark); margin-top: 2px; }

.nav { display: flex; gap: 6px; }
.nav a { padding: 8px 16px; font-size: 12px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--lcg-ink-60); text-decoration: none; border-radius: 999px; }
.nav a:hover, .nav a.active { color: var(--lcg-cream); background: var(--lcg-green); }

/* ====== Footer ====== */
footer.chrome-foot { padding: 48px; border-top: 1px solid var(--lcg-line); display: flex; justify-content: space-between; gap: 32px; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--lcg-ink-60); }

/* ====== Frame / main content ====== */
main { max-width: 1300px; margin: 0 auto; padding: 64px 48px; }

/* ====== Typography ====== */
h1, h2, h3, h4 { font-family: 'Fraunces', serif; font-weight: 300; letter-spacing: -0.03em; line-height: 1.02; margin: 0; }
h1.hero { font-weight: 200; font-size: clamp(64px, 9vw, 128px); margin-bottom: 16px; }
h2.section { font-weight: 300; font-size: clamp(40px, 5vw, 72px); margin: 80px 0 24px 0; padding-top: 32px; border-top: 1px solid var(--lcg-line); }
h2.section:first-child { border-top: none; padding-top: 0; margin-top: 32px; }
h3 { font-size: 28px; margin: 32px 0 12px 0; color: var(--lcg-dark); }
h4 { font-size: 18px; margin: 16px 0 8px 0; color: var(--lcg-dark); font-weight: 400; }
em { font-style: italic; color: var(--lcg-green); }

.eyebrow { font-family: 'Manrope', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.24em; text-transform: uppercase; color: var(--lcg-green); margin-bottom: 16px; display: inline-block; }
.meta { font-family: 'Manrope', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: var(--lcg-ink-60); }

/* ====== Stats grid ====== */
.stats { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 32px; margin: 32px 0; padding: 24px 0; border-top: 1px solid var(--lcg-line); border-bottom: 1px solid var(--lcg-line); }
.stat .num { font-family:'Fraunces', serif; font-weight: 200; font-size: 56px; line-height: 1; color: var(--lcg-dark); display: block; }
.stat .label { display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-ink-60); margin-top: 6px; }

/* ====== TOC pills ====== */
.toc { display: flex; flex-wrap: wrap; gap: 8px; margin: 32px 0; padding: 20px 0; border-top: 1px solid var(--lcg-line); border-bottom: 1px solid var(--lcg-line); }
.toc a { font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 8px 16px; border: 1px solid var(--lcg-line); border-radius: 999px; color: var(--lcg-dark); text-decoration: none; }
.toc a:hover { background: var(--lcg-green); color: var(--lcg-cream); border-color: var(--lcg-green); }
.toc a em { font-style: normal; color: var(--lcg-ink-60); font-weight: 400; margin-left: 6px; }
.toc a:hover em { color: var(--lcg-cream); }

/* ====== Bar charts (sectores/eventos) ====== */
.bars { margin: 16px 0 32px 0; }
.bar { display: grid; grid-template-columns: 200px 1fr 50px; gap: 16px; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--lcg-line); }
.bar .name { font-size: 13px; font-weight: 500; color: var(--lcg-dark); }
.bar .fill { background: rgba(3,181,133,0.18); height: 16px; border-radius: 2px; position: relative; }
.bar .fill::after { content: ''; position: absolute; left: 0; top: 0; bottom: 0; background: var(--lcg-green); border-radius: 2px; width: var(--w, 0%); }
.bar .n { text-align: right; font-family: 'Fraunces', serif; font-weight: 300; font-size: 18px; color: var(--lcg-dark); }

/* ====== Family / entity cards ====== */
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin: 24px 0 48px 0; }
.card { padding: 20px 24px; border: 1px solid var(--lcg-line); border-radius: 2px; background: rgba(242,238,232,0.6); }
.card.matched { border-color: var(--lcg-green); border-width: 1px; background: rgba(3,181,133,0.04); position: relative; }
.card.matched::before { content: '✓ CRM'; position: absolute; top: 12px; right: 14px; font-size: 9px; font-weight: 700; letter-spacing: 0.18em; color: var(--lcg-green); padding: 2px 8px; border: 1px solid var(--lcg-green); border-radius: 999px; }
.card.new::before { content: 'NUEVO'; position: absolute; top: 12px; right: 14px; font-size: 9px; font-weight: 700; letter-spacing: 0.18em; color: var(--lcg-dark); padding: 2px 8px; border: 1px solid var(--lcg-line); border-radius: 999px; }
.card.new { position: relative; }
.card .ent-name { font-family: 'Fraunces', serif; font-weight: 400; font-size: 18px; color: var(--lcg-dark); margin: 0 0 6px 0; }
.card .ent-meta { font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--lcg-ink-60); margin-bottom: 12px; }
.card .ent-meta strong { color: var(--lcg-green); }
.card .ent-dates { font-size: 12px; color: var(--lcg-ink-60); line-height: 1.6; }
.card .ent-dates .d { display: inline-block; margin-right: 8px; padding: 2px 6px; border-radius: 2px; background: rgba(8,94,84,0.06); }

/* ====== Excerpt cards ====== */
.excerpts { margin: 24px 0; }
.excerpt { padding: 24px 0; border-top: 1px solid var(--lcg-line); display: grid; grid-template-columns: 130px 1fr; gap: 32px; }
.excerpt:last-child { border-bottom: 1px solid var(--lcg-line); }
.excerpt .ex-date { font-family: 'Fraunces', serif; font-weight: 300; font-size: 22px; color: var(--lcg-dark); line-height: 1.1; }
.excerpt .ex-date small { display: block; font-family: 'Manrope', sans-serif; font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-ink-60); margin-top: 4px; }
.excerpt .ex-body { font-size: 15px; line-height: 1.7; color: var(--lcg-ink); }
.excerpt .ex-link { display: inline-block; margin-top: 12px; font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--lcg-green); text-decoration: none; }
.excerpt .ex-link:hover { color: var(--lcg-dark); }
.excerpt .ex-link::after { content: ' ↗'; }
.excerpt .ex-subtitle { font-family: 'Fraunces', serif; font-style: italic; font-size: 12px; color: var(--lcg-ink-60); margin-top: 6px; }

/* ====== Menu cards (index.html) ====== */
.menu-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin: 48px 0; }
.menu-card { display: block; padding: 32px 28px; border: 1px solid var(--lcg-line); background: rgba(242,238,232,0.4); text-decoration: none; color: inherit; border-radius: 2px; transition: all 0.15s; }
.menu-card:hover { border-color: var(--lcg-green); background: rgba(3,181,133,0.04); }
.menu-card h3 { margin-top: 0; }
.menu-card p { font-size: 14px; color: var(--lcg-ink-60); line-height: 1.5; margin: 8px 0 0 0; }
.menu-card .arrow { display: inline-block; margin-top: 12px; font-size: 11px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--lcg-green); }
.menu-card .arrow::after { content: ' →'; }

/* Estados grid in zona overview */
.state-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 32px 0; }
.state-card { display: block; padding: 24px 24px; border: 1px solid var(--lcg-line); background: rgba(242,238,232,0.6); text-decoration: none; color: inherit; }
.state-card:hover { border-color: var(--lcg-green); background: rgba(3,181,133,0.04); }
.state-card .state-name { font-family: 'Fraunces', serif; font-weight: 300; font-size: 32px; color: var(--lcg-dark); margin-bottom: 8px; }
.state-card .state-stats { font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--lcg-ink-60); }
.state-card .state-stats strong { color: var(--lcg-green); font-weight: 700; }

/* Print */
@media print {
    header.chrome, .toc { display: none; }
    main { padding: 32px; max-width: 100%; }
}
"""


def render_bars(items: list[tuple[str, int]], max_n: int = None) -> str:
    if not items:
        return '<p class="meta">Sin datos suficientes en los extractos.</p>'
    max_n = max_n or max(n for _, n in items)
    bars = []
    for name, n in items:
        pct = (n / max_n * 100) if max_n else 0
        bars.append(f'<div class="bar"><span class="name">{html.escape(name)}</span><span class="fill" style="--w: {pct:.0f}%;"></span><span class="n">{n}</span></div>')
    return '<div class="bars">' + ''.join(bars) + '</div>'


def render_excerpt(ex: dict) -> str:
    text = html.escape(ex["text"])
    # Truncate excerpt if super long (>600 chars)
    if len(text) > 700:
        text = text[:680] + "…"
    return f"""<article class="excerpt">
    <div class="ex-date">{html.escape(ex["date"])}
        <small>{html.escape(ex["subtitle"][:55])}</small>
    </div>
    <div class="ex-body">
        <p>{text}</p>
        <a class="ex-link" href="{html.escape(ex["url"])}" target="_blank">Abrir post completo en Whitepaper</a>
    </div>
</article>"""


def render_state_page(intel: dict) -> str:
    st = intel["state"]
    crm = intel["crm"]

    # Family cards (mencionadas + no mencionadas)
    fam_cards = []
    mentioned_labels = set(intel["ppt_families_mentioned"].keys())
    for label, aliases in PPT_FAMILIAS.get(st, []):
        if label in mentioned_labels:
            mentions = intel["ppt_families_mentioned"][label]
            count = len(mentions)
            dates_html = "".join(f'<span class="d">{html.escape(m["date"])}</span>' for m in mentions[:6])
            fam_cards.append(f"""<div class="card matched">
    <h4 class="ent-name">{html.escape(label)}</h4>
    <div class="ent-meta"><strong>{count}</strong> mención{"es" if count > 1 else ""} · más reciente: {html.escape(mentions[0]["date"])}</div>
    <div class="ent-dates">{dates_html}</div>
</div>""")
    if not fam_cards:
        fam_cards.append('<p class="meta">Ninguna de las familias del PPT apareció en los posts. Revisar manualmente.</p>')

    # New entities
    new_ent_cards = []
    for ent, n in intel["new_entities"][:24]:
        new_ent_cards.append(f"""<div class="card new">
    <h4 class="ent-name">{html.escape(ent)}</h4>
    <div class="ent-meta"><strong>{n}</strong> mención{"es" if n > 1 else ""} en extractos del estado</div>
</div>""")
    if not new_ent_cards:
        new_ent_cards.append('<p class="meta">No se detectaron nuevas referencias con frecuencia ≥ 2.</p>')

    # Excerpts
    ex_html = "".join(render_excerpt(ex) for ex in intel["excerpts"])

    # Familias del PPT no mencionadas (para playbook)
    not_mentioned = [label for label, _ in PPT_FAMILIAS.get(st, []) if label not in mentioned_labels]
    not_mentioned_html = ""
    if not_mentioned:
        items = "".join(f'<li>{html.escape(n)}</li>' for n in not_mentioned)
        not_mentioned_html = f'<h4>Familias del PPT NO mencionadas en Whitepaper (oportunidades de inteligencia complementaria)</h4><ul style="font-size:13px;color:var(--lcg-ink-60);">{items}</ul>'

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>{html.escape(st)} · Inteligencia Comercial · LCG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head><body>
{chrome_header(active='zona')}
<main>
    <span class="eyebrow">Inteligencia comercial · Zona Sur-Centro-Golfo</span>
    <h1 class="hero">{html.escape(st)}.</h1>
    <p class="meta">{html.escape(crm["industries"])}</p>

    <div class="stats">
        <div class="stat"><span class="num">{crm["aaa_aa"]}</span><span class="label">AAA+AA CRM</span></div>
        <div class="stat"><span class="num">{crm["dm"]}</span><span class="label">Decision makers</span></div>
        <div class="stat"><span class="num">{intel["total_excerpts"]}</span><span class="label">Extractos Whitepaper</span></div>
        <div class="stat"><span class="num">{intel["ppt_families_hit"]}/{intel["ppt_families_total"]}</span><span class="label">Familias PPT mencionadas</span></div>
        <div class="stat"><span class="num">{len(intel["new_entities"])}</span><span class="label">Nuevas referencias</span></div>
    </div>

    <h2 class="section">Tendencias <em>recientes</em></h2>
    <h3>Sectores más mencionados en los extractos del estado</h3>
    {render_bars(intel["top_sectors"])}

    <h3>Tipos de evento más frecuentes</h3>
    {render_bars(intel["top_events"])}

    <h2 class="section">Familias del CRM <em>mencionadas</em></h2>
    <p class="meta">Cruce con las {intel["ppt_families_total"]} familias/empresas del PPT consolidado Sur-Centro-Golfo.</p>
    <div class="cards">{''.join(fam_cards)}</div>
    {not_mentioned_html}

    <h2 class="section">Nuevas <em>referencias</em> detectadas</h2>
    <p class="meta">Entidades con 2+ menciones en extractos del estado que NO están en la lista del PPT. Posibles leads para investigar.</p>
    <div class="cards">{''.join(new_ent_cards)}</div>

    <h2 class="section">Extractos <em>textuales</em></h2>
    <p class="meta">Párrafos donde aparece el estado o una de sus ciudades. Orden cronológico inverso.</p>
    <div class="excerpts">{ex_html}</div>

</main>
{chrome_footer()}
</body></html>"""


# ========================================================================
# ZONA OVERVIEW (zona.html)
# ========================================================================

def render_zona_overview(state_intels: list[dict]) -> str:
    cards = []
    total_excerpts = 0
    total_families_hit = 0
    total_new_entities = 0
    for intel in state_intels:
        st = intel["state"]
        slug = slugify(st)
        total_excerpts += intel["total_excerpts"]
        total_families_hit += intel["ppt_families_hit"]
        total_new_entities += len(intel["new_entities"])
        cards.append(f"""<a class="state-card" href="estado-{slug}.html">
    <h3 class="state-name">{html.escape(st)}</h3>
    <div class="state-stats">
        <strong>{intel["total_excerpts"]}</strong> extractos ·
        <strong>{intel["ppt_families_hit"]}/{intel["ppt_families_total"]}</strong> familias PPT ·
        <strong>{len(intel["new_entities"])}</strong> nuevas refs
    </div>
</a>""")

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>Zona Sur-Centro-Golfo · Inteligencia Comercial · LCG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head><body>
{chrome_header(active='zona')}
<main>
    <span class="eyebrow">Iniciativa comercial · 11 estados</span>
    <h1 class="hero">Zona <em>Sur-Centro-Golfo</em>.</h1>
    <p class="meta">Inteligencia comercial extraída de 247 posts de Whitepaper.mx (mayo 2025 → mayo 2026). Cada estado tiene su deep dive: tendencias, familias del CRM mencionadas, nuevas referencias detectadas y extractos textuales de las noticias.</p>

    <div class="stats">
        <div class="stat"><span class="num">11</span><span class="label">Estados</span></div>
        <div class="stat"><span class="num">294</span><span class="label">AAA+AA en CRM</span></div>
        <div class="stat"><span class="num">650</span><span class="label">Decision makers</span></div>
        <div class="stat"><span class="num">{total_excerpts}</span><span class="label">Extractos totales</span></div>
        <div class="stat"><span class="num">{total_families_hit}/62</span><span class="label">Familias PPT mencionadas</span></div>
        <div class="stat"><span class="num">{total_new_entities}</span><span class="label">Nuevas referencias</span></div>
    </div>

    <h2 class="section">Estados</h2>
    <p class="meta">Click en un estado para ver su intel comercial completa.</p>
    <div class="state-grid">{''.join(cards)}</div>
</main>
{chrome_footer()}
</body></html>"""


# ========================================================================
# INDEX / MENU (index.html)
# ========================================================================

def render_index(state_intels: list[dict]) -> str:
    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>Whitepaper Intelligence · LCG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head><body>
{chrome_header(active='inicio')}
<main>
    <span class="eyebrow">London Consulting Group · Market Intelligence</span>
    <h1 class="hero">Whitepaper, <em>Hoy</em>.</h1>
    <p class="meta">Inteligencia comercial de Whitepaper.mx aplicada a la iniciativa Zona Sur-Centro-Golfo · 247 posts · Mayo 2025 → Mayo 2026</p>

    <div class="menu-grid">
        <a class="menu-card" href="zona.html">
            <h3>Zona Sur-Centro-Golfo</h3>
            <p>11 estados · 294 AAA+AA · deep dive por estado con tendencias, familias del CRM, nuevas referencias y extractos textuales.</p>
            <span class="arrow">Inteligencia por estado</span>
        </a>
        <a class="menu-card" href="categorias.html">
            <h3>Por categoría</h3>
            <p>247 posts taggeados por 14 sectores y 10 tipos de evento. Útil para encontrar todos los posts sobre M&A, automotriz, fintech, etc.</p>
            <span class="arrow">Inteligencia transversal</span>
        </a>
        <a class="menu-card" href="brief.html">
            <h3>Brief consolidado</h3>
            <p>Documento maestro con los 247 posts en orden cronológico. Para leer secuencialmente o exportar a PDF.</p>
            <span class="arrow">Documento completo</span>
        </a>
    </div>

    <h2 class="section">Estados <em>de la zona</em></h2>
    <p class="meta">Acceso directo a la inteligencia comercial de cada estado.</p>
    <div class="state-grid">{''.join(f'<a class="state-card" href="estado-{slugify(i["state"])}.html"><h3 class="state-name">{html.escape(i["state"])}</h3><div class="state-stats"><strong>{i["total_excerpts"]}</strong> extractos · <strong>{i["ppt_families_hit"]}/{i["ppt_families_total"]}</strong> familias</div></a>' for i in state_intels)}</div>
</main>
{chrome_footer()}
</body></html>"""


# ========================================================================
# MAIN
# ========================================================================

def main():
    print("="*72)
    print("STATE INTELLIGENCE v2 — Inteligencia comercial por estado")
    print("="*72)

    posts = load_posts()
    if not posts:
        print(f"ERROR: no posts en {POSTS_DIR}")
        return
    print(f"  Cargados: {len(posts)} posts")

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)

    # Build intel per state
    state_intels = []
    for st in ZONA_ESTADOS:
        print(f"  → {st}...", end=" ")
        intel = build_state_intel(st, posts)
        state_intels.append(intel)
        print(f"{intel['total_excerpts']} extractos · {intel['ppt_families_hit']}/{intel['ppt_families_total']} familias · {len(intel['new_entities'])} nuevas refs")

    # Render per-state pages
    print("  Renderizando páginas por estado...")
    for intel in state_intels:
        slug = slugify(intel["state"])
        (DOCS / f"estado-{slug}.html").write_text(render_state_page(intel), encoding="utf-8")

    # Render zona overview
    (DOCS / "zona.html").write_text(render_zona_overview(state_intels), encoding="utf-8")
    print(f"  ✓ docs/zona.html")

    # Render index/menu
    (DOCS / "index.html").write_text(render_index(state_intels), encoding="utf-8")
    print(f"  ✓ docs/index.html")

    # Write shared CSS
    (DOCS / "styles.css").write_text(CSS, encoding="utf-8")
    print(f"  ✓ docs/styles.css")

    # Copy brief/categorias from output/ (siempre que existan)
    for src_name, dst_name in [("brief.html", "brief.html"), ("categorias.html", "categorias.html")]:
        src = OUT / src_name
        if src.exists():
            # Reemplazo el contenido del HTML para que use el chrome unificado
            # (Por ahora simplemente lo copio tal cual; el menú no aparecerá en esas páginas)
            dst = DOCS / dst_name
            shutil.copy(src, dst)
            print(f"  ✓ docs/{dst_name} (copiado desde output/)")

    print("="*72)
    print(f"LISTO · docs/ contiene {len(list(DOCS.glob('*.html')))} páginas HTML")
    print("Abre docs/index.html en tu navegador")


if __name__ == "__main__":
    main()
