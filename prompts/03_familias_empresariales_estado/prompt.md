# Prompt 03 — Familias empresariales del estado

## Objetivo
Generar el archivo `estados/<estado>/03_familias_empresariales.md` con un mapa de las **familias empresariales** que históricamente controlan o influyen en la economía del estado.

Este archivo es **fundamental para LCG porque la consultoría operativa muchas veces toca temas de gobierno corporativo y profesionalización de empresas familiares**. Entender los apellidos del poder local es decisivo.

## Instrucciones para Claude Code

### Marco conceptual
- México es un país donde **la economía es marcadamente familiar**. En cada estado hay un puñado de apellidos que controlan buena parte del PIB local.
- Algunas familias son **muy públicas** (Slim, Salinas Pliego, Bailleres, Larrea, Azcárraga). Otras son **regionales y mucho más discretas** (Ponce y Vales en Yucatán, Robinson Bours en Sonora, Coppel en Sinaloa, etc.).
- Para cada estado hay **familias autóctonas** (su poder se origina ahí) y **familias nacionales con presencia fuerte** (que tienen operaciones grandes ahí).

### Estructura del archivo

#### Sección A — Familias originarias del estado
Familias cuyo poder económico **nació en este estado**. Para cada una:

```markdown
### Familia <Apellido(s)>

| Campo | Detalle |
|-------|---------|
| Apellido(s) principal(es) | <ej. Vales / Ponce / Bailleres> |
| Origen | <ciudad, estado, época> |
| Generación actual al mando | <1ª / 2ª / 3ª / 4ª+> |
| Patriarca / Matriarca | <nombre, edad si pública> |
| Sucesores activos | <nombres y roles> |
| Sector(es) económico(s) | <listado> |
| Empresas / grupos que controla | <listado, marcar cotizadas si aplica> |
| Patrimonio estimado | <USD o MDP si hay fuente; si no, `[NO DISPONIBLE]`> |
| Presencia en consejos de otras compañías | <listado si aplica> |
| Filantropía / fundaciones | <si las hay> |
| Visibilidad pública | Alta / Media / Baja |

**Narrativa (3-6 párrafos):**
- Origen del patrimonio (qué negocio fundacional)
- Hitos en la historia del grupo familiar
- Transición generacional: ¿la siguiente generación está tomando control? ¿están profesionalizando?
- Disputas conocidas (escisiones, conflictos sucesorios, divisiones del grupo)
- Relación con otras familias del estado (alianzas, matrimonios, joint ventures)
- Relación con el poder político local
- Movimientos recientes (M&A, ventas de activos, nuevos proyectos)

**Pistas para LCG (sin recomendar outreach):**
- ¿Está la familia en proceso de profesionalización o sucesión?
- ¿Hay señales de necesidades de gobierno corporativo?
- ¿La siguiente generación tiene formación profesional (Harvard, IPADE, etc.)?

**Fuentes específicas:** ...
```

Mínimo 5 familias si el estado lo permite. En CDMX, EdoMex y Veracruz puede haber 15-25 familias relevantes. En estados pequeños, 3-7.

#### Sección B — Familias nacionales con peso en el estado
Familias del poder económico nacional cuyas operaciones más relevantes en el país tocan este estado de forma significativa.

Tabla resumida:

| Familia | Empresas / grupos | Operación relevante en este estado |
|---------|------------------|----------------------------------|

#### Sección C — Mapa de cruces familiares
- Matrimonios entre familias relevantes que se traduzcan en alianzas empresariales
- Hijos/as de una familia trabajando en empresas de otra
- Consejos compartidos
- Cámaras donde se cruzan (presidencias rotativas, ej. COPARMEX estatal)

#### Sección D — La "vieja guardia" vs la "nueva generación"
- Familias en transición sucesoria
- Patrimonios que se están fragmentando
- Apellidos emergentes (segunda o tercera generación que están dejando huella propia)

#### Sección E — Notas de contexto
- Familias con discreción extrema (no aparecen en Forbes pero todos en la ciudad saben quiénes son)
- Familias controvertidas (juicios, escándalos, conflictos con autoridades)
- Familias con familiares en el extranjero relevantes para entender la operación

## Formato
- Markdown
- Mínimo 1,200 palabras, idealmente 2,000-3,500
- Más narrativa que tablas (las familias son historias)
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
- Forbes México (especialmente la lista anual de millonarios)
- Bloomberg Billionaires Index (para los más grandes)
- Mexico Business News, Bloomberg Línea
- Reportes de KPMG / PwC / EY sobre empresas familiares en México
- IPADE family business reports
- Prensa regional del estado (un periódico local suele saber más que un nacional)
- LinkedIn de miembros de la familia
- Sitios de fundaciones familiares
- BMV / SEC para grupos cotizados

## No hagas
- **No inventes apellidos, parentescos, montos de patrimonio o conflictos familiares.** Esta es información sensible.
- No publiques chismes sin fuente.
- Si la información sobre una familia es muy escasa, mejor incluye menos familias con más profundidad que muchas familias con datos pobres.
- No describas tensiones familiares como hechos si solo son rumores. Usa lenguaje como `[Trascendido en prensa: ...]`.
- No clasifiques familias como "objetivos" de LCG. Solo descripción.
