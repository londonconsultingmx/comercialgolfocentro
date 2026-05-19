# Prompt 05 — Cámaras, asociaciones y clusters del estado

## Objetivo
Generar el archivo `estados/<estado>/05_camaras_y_clusters.md` con un mapa del **ecosistema institucional empresarial** del estado: cámaras, asociaciones, consejos, clusters productivos, alumni networks.

Este archivo es **práctico**: identifica los espacios donde se mueven los decisores empresariales del estado, eventos clave, presidencias rotativas, y formas de entrar al círculo.

## Instrucciones para Claude Code

### Estructura del archivo

#### Sección A — Cámaras y organismos cúpula

```markdown
### <Nombre del organismo, ej. COPARMEX Yucatán>

| Campo | Detalle |
|-------|---------|
| Tipo | Cámara / Asociación / Consejo / Cluster / Fundación |
| Sede | <ciudad> |
| Año de fundación | <año> |
| Número aproximado de afiliados | <#> |
| Presidente actual | <nombre, hasta cuándo> |
| Presidente anterior | <nombre> |
| Director general / ejecutivo | <nombre> |
| Sectores que agrupa | <listado> |
| Cuotas / membresía | <si dato público> |
| Eventos anuales clave | <listado: Foro X, Congreso Y> |
| Sitio web | URL |

**Por qué importa:**
- Influencia política y económica local
- Quiénes lo presiden suelen ser CEOs de grupos relevantes (mapa de poder)
- Eventos de la cámara son terreno natural para conocer decisores
- Presidencias rotativas: ver quién ha pasado por ahí en los últimos 5 años revela el "círculo interno"
```

Cubre los relevantes para el estado:
- **CCE** estatal (Consejo Coordinador Empresarial)
- **COPARMEX** estatal
- **CANACINTRA** estatal (donde haya manufactura)
- **CAINTRA** (Nuevo León y similares — en este proyecto aplica menos pero verifica)
- **CMIC** (construcción)
- **ANTAD** (retail, si aplica)
- **CCE/Canaco** locales
- Cámaras sectoriales con presencia estatal fuerte (AMIA, ANIPAC, CANIETI, ANIQ, CMP, AMIPCI, AMECE, etc.)
- Consejos turísticos / hoteleros donde aplique
- Asociaciones de FIBRAS, family offices o agroexportadores cuando relevante

#### Sección B — Clusters productivos y consejos sectoriales
- Clusters automotrices, aeronáuticos, eléctrico-electrónicos, de software, agroalimentarios
- Identifica gobernadores activos: directores ejecutivos del cluster y empresas líderes

| Cluster | Sector | Director ejecutivo | Empresas ancla | Ubicación |
|---------|--------|-------------------|----------------|-----------|

#### Sección C — Alumni networks relevantes en el estado
Las redes universitarias son uno de los puentes más poderosos en México:

| Universidad / red | Presencia en el estado | Eventos / capítulos | Decisores conocidos egresados |
|-------------------|----------------------|---------------------|-------------------------------|

Cubre al menos:
- **IPADE** Business School
- **ITAM**
- **Tec de Monterrey** (campus locales relevantes)
- **Universidad Anáhuac**
- **UDLAP** (Puebla)
- **Universidad Iberoamericana**
- Universidades locales relevantes (UADY en Yucatán, UANL en el norte, UJAT en Tabasco, etc.)
- Programas internacionales (Harvard alumni, Wharton, INSEAD, MIT) si tienen capítulo local

#### Sección D — Family offices y clubes de inversión locales
Algunos estados tienen family offices establecidos o "wealth advisory" donde se cruzan las grandes familias. Incluye los que tengan presencia pública.

#### Sección E — Eventos clave del calendario anual
Mapa de eventos a los que asisten los decisores empresariales del estado:

| Evento | Mes típico | Organizador | Tipo de asistente | Relevancia |
|--------|-----------|-------------|-------------------|-----------|

Ej: Foro Anual COPARMEX, Reunión Nacional CCE, Tianguis Turístico, INA Expo, EXPO Manufactura, etc.

#### Sección F — El "círculo interno" del estado
Identifica al subgrupo de personas que **se cruzan en múltiples cámaras / consejos / clubes** — son el verdadero centro de gravedad empresarial del estado. Si X persona preside una cámara, está en el consejo de dos empresas y participa en una fundación, es alguien estratégicamente relevante.

## Formato
- Markdown
- Mínimo 800 palabras, idealmente 1,500-2,500
- Tablas + narrativa
- Sección final: **"Fuentes consultadas"**


## Convenciones de escritura para que el render visual quede limpio

Los `.md` que generes serán convertidos a HTML/PDF estilizado LCG. Por favor:

1. **Usa cursiva markdown (`*texto*`)** para destacar nombres clave (familias, grupos, conceptos importantes, cifras notables). Estos se renderizan en **cursiva verde**, que es el acento institucional del documento.
2. **Tablas en lugar de bullets** cuando haya datos comparables (3+ ítems con atributos paralelos).
3. **Blockquotes (`>`)** para insights destacados que quieras que sobresalgan visualmente.
4. **H4 como "eyebrow"** para etiquetas tipo `#### Insight clave`, `#### Fuentes consultadas`, `#### Contexto`.
5. **Separa secciones con `---`** (renderiza como línea divisoria sutil entre bloques de contenido).
6. **Negritas (`**texto**`)** solo para énfasis fuerte dentro de párrafos, no para títulos.
7. **Un solo H1** por archivo (el título principal).
8. **Sin emojis decorativos.**

Ejemplo de uso:

```markdown
# Familias empresariales — Yucatán

#### Contexto

En *Yucatán* el poder económico se concentra en *3-4 familias troncales* con presencia transversal en banca, retail y agroindustria.

> El poder se hereda, no se reparte.

---

## Familia *Vales*

| Atributo | Detalle |
|---|---|
| Generación actual | 3ª |
| Sectores | Banca, retail, agroindustria |
| Sede | Mérida |
```

Ver `styles/SISTEMA_VISUAL.md` para la guía completa.

## Fuentes prioritarias
- Sitios web de cada cámara
- LinkedIn (presidentes y consejos directivos)
- Notas de prensa sobre tomas de protesta de presidentes
- IMEF (Instituto Mexicano de Ejecutivos de Finanzas) si tiene capítulo local
- Cámaras binacionales (AmCham, BritCham, CCFM) si aplica
- Reportes de la cámara cuando los publican

## No hagas
- No publiques cuotas de membresía si no tienes fuente.
- No asumas presidencias actuales sin verificar fecha (las cámaras rotan rápido).
- Si un cluster está casi muerto pero existe formalmente, dilo.
