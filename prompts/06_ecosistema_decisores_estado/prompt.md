# Prompt 06 — Ecosistema de decisores del estado

## Objetivo
Generar el archivo `estados/<estado>/06_ecosistema_decisores.md`: el mapa nominal de las **personas que toman decisiones empresariales relevantes** en el estado.

Este archivo es el más sensible y el más útil. Aquí están los nombres.

## Instrucciones para Claude Code

### Marco conceptual
Hay **tres tipos de decisores** que hay que identificar:

1. **C1 — Dueños / fundadores / patriarcas/matriarcas / presidentes del consejo.** Toman decisiones de fondo: rumbo del grupo, sucesión, M&A, expansión.
2. **C2 — CEOs, Directores Generales, CFOs y COOs profesionales** (sean o no de la familia controladora). Toman decisiones operativas y comparten poder con C1.
3. **C3 — Líderes de cámaras, consejos y clusters.** No siempre son los más ricos, pero modulan el ambiente del estado y son puentes naturales.

### Estructura del archivo

#### Sección A — Top decisores absolutos del estado (15-25 personas)
Las personas más influyentes del estado, sin importar el sector. Para cada una:

```markdown
### <Nombre completo>

| Campo | Detalle |
|-------|---------|
| Categoría | C1 / C2 / C3 |
| Rol(es) principal(es) | <ej. Presidente del Consejo, Grupo X> |
| Empresa(s) que controla o dirige | <listado> |
| Familia (si aplica) | <apellido familiar> |
| Edad aproximada | <si pública> |
| Formación | <universidades, programas ejecutivos> |
| Origen / ciudad | <si conocido> |
| Visibilidad pública | Alta / Media / Baja |
| LinkedIn | <URL si pública> |

**Trayectoria breve (2-3 párrafos):**
- Cómo llegó a la posición actual
- Hitos profesionales o empresariales
- Otras compañías donde ha estado en el consejo o ha trabajado

**Señales recientes (últimos 12 meses):**
- Declaraciones públicas
- Anuncios de su empresa que pueden ser vistos como "su" decisión
- Movimientos en consejos
- Reconocimientos públicos
- Asistencia a foros importantes

**Cruces con otras personas del mapa:**
- Familias o decisores con los que tiene relación pública
- Cámaras donde coincide con otros C1/C2

**Notas para LCG (sin recomendar outreach):**
- Si la persona ha sido cliente o referido de LCG (consultar `data/crm/hubspot_contactos.csv`)
- Si está en proceso de sucesión / profesionalización
- Si tiene estilo conservador o disruptivo
```

#### Sección B — Mapa de decisores por sector dominante del estado
Después de los 15-25 generales, profundiza por sector. Para cada sector clave del estado identificado en `04_sectores_clave.md`, lista los decisores top del sector (5-10 por sector):

```markdown
## Decisores en sector <X>

| Nombre | Empresa / cargo | Categoría | Notas clave |
|--------|----------------|-----------|-------------|
```

#### Sección C — Personas C3 (presidentes de cámaras y consejos)
Tabla completa de quién preside actualmente las cámaras / consejos / clusters que identificaste en `05_camaras_y_clusters.md`:

| Persona | Cámara / Consejo | Rol | Vigencia del cargo | Empresa propia / cargo principal |
|---------|------------------|-----|-------------------|----------------------------------|

#### Sección D — Cruce con CRM de LCG
Lee `data/crm/hubspot_contactos.csv` filtrado por el estado del estudio. Identifica:

1. **Decisores ya conocidos por LCG** que aparezcan en tu mapa. Marca con "✓ Contacto previo en CRM" y agrega: propietario LCG, etapa, última actividad.
2. **Decisores en tu mapa que NO aparecen en el CRM** — flag como "Hueco blanco en CRM".

| Decisor | En CRM | Owner LCG | Etapa | Última actividad |
|---------|--------|-----------|-------|------------------|

⚠️ **No publiques correos electrónicos en este archivo** (es información sensible que puede acabar en commits / shares). Solo señala si está en CRM y bajo qué propietario.

#### Sección E — Red de poder visible
Diagrama o descripción narrativa de las **conexiones cruzadas**: quién está en el consejo de quién, quién es socio de quién, quién es padre/hijo/hermano de quién (solo información pública).

#### Sección F — Próxima generación (next gen)
Identifica a hijos/as o sucesores que están tomando posiciones de poder. Son los decisores de los próximos 10-15 años.

## Formato
- Markdown
- Mínimo 1,500 palabras, idealmente 3,000-5,000 (este suele ser el archivo más largo)
- Tablas + fichas de persona
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
- LinkedIn (perfiles públicos)
- Sitios corporativos (sección "About Us" / "Consejo de Administración")
- BMV / SEC para empresas públicas (consejos de administración listados en reportes anuales)
- Forbes México (lista de millonarios)
- Entrevistas en El Financiero, Bloomberg Línea, Expansión, Forbes
- Reportes de cámaras
- Notas sociales (los decisores aparecen en eventos sociales documentados)
- `data/crm/hubspot_contactos.csv` para cruce

## No hagas
- **No publiques correos, celulares o información de contacto privada.** Aunque aparezca en el CRM, este archivo es para mapeo, no para contacto directo.
- **No inventes relaciones familiares, edades, o trayectorias.** Si no encuentras el dato, dilo.
- No clasifiques personas como "fáciles" o "difíciles" de abordar. Solo descripción factual.
- Si una persona tiene controversias públicas (juicios, investigaciones), descríbelas con lenguaje neutro y con fuente. No editorices.
- No incluyas personas que solo trabajen en gobierno (este estudio es empresarial). Excepción: ex-gobernadores que ahora estén en empresas privadas grandes.
