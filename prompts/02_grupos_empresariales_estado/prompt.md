# Prompt 02 — Grupos empresariales del estado

## Objetivo
Generar el archivo `estados/<estado>/02_grupos_empresariales.md` con un mapa profundo de los **grupos empresariales, holdings y conglomerados** que operan o tienen sede en el estado.

Este es uno de los archivos más importantes del proyecto. Aquí se identifica **quién controla qué** en términos económicos.

## Instrucciones para Claude Code

### Distinción importante
- **Grupo empresarial / holding**: estructura corporativa que controla múltiples empresas operativas. Ej: Grupo Carso, FEMSA, Grupo BAL, ALFA, Vitro, Grupo Vasconia.
- **Empresa individual relevante** (no es un grupo pero es muy grande): NO va aquí. Va en `07_empresas_top_30.md`.

### Estructura del archivo

#### Sección A — Grupos con sede corporativa en el estado
Identifica los grupos cuya **sede corporativa** está en el estado. Para cada uno produce una mini-ficha:

```markdown
### Grupo <Nombre>

| Campo | Detalle |
|-------|---------|
| Sede corporativa | <ciudad>, <estado> |
| Fundación | <año> |
| Dueño / familia controladora | <apellido o nombre> |
| Naturaleza | Pública (BMV/SEC) / Privada / Familiar |
| Facturación estimada | <MDP o USD, año> |
| Empleados | <#> |
| Empresas operativas que controla | <listado> |
| Sectores que toca | <listado> |
| Cobertura geográfica | Nacional / Internacional / Estatal |

**Perfil narrativo (3-5 párrafos):**
- Historia y trayectoria del grupo
- Modelo de negocio y estructura de control
- Momentum reciente (últimos 24 meses): M&A, expansiones, anuncios, cambios directivos
- Relación con otras familias o grupos del estado
- Notas relevantes para LCG (sin recomendar acción, solo flags útiles)

**Fuentes específicas para este grupo:** ...
```

Mínimo 5 grupos si el estado lo permite, hasta 15 grupos. **En CDMX y Estado de México puede haber 20+.** En estados pequeños (Tlaxcala-tamaño), puede haber 3-4. Sé honesto con la realidad de cada estado.

#### Sección B — Grupos con presencia operativa relevante (sede en otro lado)
Grupos nacionales o internacionales cuya sede está fuera del estado pero tienen **operaciones de gran tamaño** en este estado (plantas, divisiones, centros logísticos importantes). Mini-ficha más corta:

| Grupo | Sede corp. | Operación en este estado | Empresas / plantas / divisiones |
|-------|-----------|-------------------------|-------------------------------|

Mínimo 5, hasta 20 dependiendo del estado.

#### Sección C — Mapa de relaciones cruzadas
- Familias o grupos que comparten consejos de administración entre sí
- Empresas del estado donde participan grupos foráneos (alianzas, joint ventures, M&A recientes)
- Family offices del estado (si los hay y son públicos)

#### Sección D — Tendencias del ecosistema
- ¿Qué grupos están en expansión activa?
- ¿Qué grupos están vendiendo activos / sucediendo / en transición?
- ¿Hay grupos emergentes (segunda o tercera generación) que estén tomando protagonismo?
- ¿Hay fondos de PE locales activos?

## Formato
- Markdown
- Mínimo 1,200 palabras, idealmente 2,000-3,000
- Tablas + narrativa, no solo tablas
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
- Ranking Expansión 500 (filtrar por sede o presencia en el estado) — `data/expansion/`
- Sitios web corporativos de cada grupo
- BMV / SEC para grupos públicos
- LinkedIn de los grupos
- Notas de prensa: El Financiero, El Economista, Expansión, Forbes México, Bloomberg Línea, Mexico Business News
- CCE estatal, COPARMEX estatal (a veces publican rankings o consejos directivos)
- Reportes de KPMG / EY / Deloitte sobre empresas familiares
- **CSVs del CRM** en `data/crm/` para identificar grupos ya tocados por LCG (úsalos como insumo, no los publiques verbatim)

## No hagas
- No inventes propietarios de empresas privadas. Si no encuentras al dueño en fuentes públicas, escribe `[Propietario no identificado en fuentes públicas — verificar en reunión de descubrimiento]`.
- No incluyas estimaciones de facturación de empresas privadas sin marcar `[ESTIMACIÓN]`.
- No clasifiques grupos en "Tier A/B/C" ni recomiendes outreach.
- No mezcles grupos de un estado con otro. Si un grupo tiene sede en CDMX pero opera en Yucatán, va en CDMX (Sección A) y en Yucatán (Sección B).
