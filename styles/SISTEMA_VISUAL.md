# Sistema Visual LCG

> Versión 1.0 · Mayo 2026
> Aplicable a: presentaciones HTML, exports PDF, conversiones de los `.md` del proyecto.

---

## Paleta institucional

| Token | Hex / RGBA | Uso |
|---|---|---|
| `--lcg-dark` | `#085E54` | Verde institucional oscuro — titulares, divisores dark, fondo de portada |
| `--lcg-green` | `#03B585` | Verde LCG — acentos, eyebrows, números, énfasis |
| `--lcg-mint` | `#8AF4E9` | Mint — highlights sobre dark, énfasis sobre fondo verde oscuro |
| `--lcg-cream` | `#F2EEE8` | Crema cálida — fondo principal (reemplaza blanco puro) |
| `--lcg-ink` | `#1A1E1B` | Texto primario — casi negro, nunca negro puro |
| `--lcg-ink-60` | `rgba(26,30,27,0.62)` | Texto secundario, breadcrumbs, fechas |
| `--lcg-line` | `rgba(8,94,84,0.18)` | Líneas divisorias sutiles |

**Regla:** nunca blanco puro. Siempre crema. Dark backgrounds solo para section dividers y cover-green.

---

## Tipografía

### Familias
- **Fraunces** (serif, weights 200/300/400) → titulares grandes, números display, `<em>` para cursiva verde de acento
- **Manrope** (sans, 400/500/600/700) → body, meta, eyebrows, UI

### Escala

| Elemento | Tamaño | Familia | Peso | Tracking | Line-height |
|---|---|---|---|---|---|
| h1 | 148-160px | Fraunces | 200 | -0.03em | 0.98 |
| h2 | 96px | Fraunces | 300 | -0.03em | 1.00 |
| h3 | 64px | Fraunces | 400 | -0.03em | 1.05 |
| body | 28px | Manrope | 400 | 0 | 1.45 |
| small | 22px | Manrope | 400 | 0 | 1.5 |
| meta | 14-16px | Manrope | 500 | 0.16em | 1.0 |
| num-big | 300-500px | Fraunces | 200 | -0.04em | 0.9 |

**Reglas clave:**
- Todos los titulares con `letter-spacing: -0.03em` y `line-height: 0.98-1.05`
- Meta y eyebrows siempre en `uppercase` con `letter-spacing: 0.16em`
- `<em>` dentro de h1/h2/h3 = cursiva verde (acento institucional)

---

## Composición

### Frame institucional
Cada slide o página principal usa este wrapper:

```html
<div class="frame">
  <div class="chrome-top">
    <span class="section-label">Yucatán · Familias</span>
    <span class="emblem"></span>
  </div>

  <h1>Los <em>Vales</em> & <em>Ponce</em></h1>
  <p>Contenido principal...</p>

  <div class="chrome-bottom">
    <span class="breadcrumb">Estados / Yucatán / Familias</span>
    <span class="slide-num">03 / 24</span>
  </div>
</div>
```

### Padding institucional
`80px 100px` — respiración consultiva. Reservado para presentaciones; para documentos largos (`.doc`) el padding es menor.

### Grid
Preferencia por `grid-template-columns: 440px 1fr` (label + content) en slides analíticas.

---

## Componentes

### Pills

```html
<span class="pill">AAA</span>
<span class="pill outline">Lead Calificado</span>
```

- `border-radius: 999px` (siempre redondeados completos)
- Fondo `--lcg-green` o borde verde
- Texto en `--lcg-cream` (sólido) o `--lcg-dark` (outline)

### Cards

```html
<div class="card">
  <p class="card-meta">Grupo Empresarial</p>
  <h3 class="card-title">Grupo <em>Vales</em></h3>
  <p class="card-body">Banca, retail, agroindustria...</p>
</div>
```

- `border: 1px solid var(--lcg-line)`
- Sin sombras
- Sin radius o radius: 4px máximo

### Tablas

- `border-bottom` sutil con `--lcg-line`
- Sin zebra (alternancia de filas)
- `th` en `uppercase` con `letter-spacing: 0.16em`, color `--lcg-green`
- Primera columna con `font-weight: 500`

```markdown
| Empresa | Sector | Sede |
|---|---|---|
| Grupo Vales | Banca, retail | Mérida |
```

### Números grandes (num-big)

```html
<div class="num-big">$11.5MMDP</div>
<div class="num-big cream">12</div>
```

- Fraunces weight 200
- Tamaño 300-500px (responsivo)
- Color verde (`--lcg-green`) o crema (sobre dark)

### Section divider

Banda dark institucional entre capítulos:

```html
<div class="section-divider">
  <p class="section-eyebrow">Capítulo 03</p>
  <h2 class="section-title">Familias <em>empresariales</em></h2>
</div>
```

### Cover green

Portada institucional con fondo verde oscuro:

```html
<div class="cover-green">
  <div class="chrome-top">
    <span class="section-label">LCG · Market Intelligence</span>
    <span class="emblem"></span>
  </div>

  <div>
    <p class="meta">Estudio de zona</p>
    <h1>Yucatán</h1>
    <p>El ecosistema empresarial del sureste mexicano</p>
  </div>

  <div class="chrome-bottom">
    <span class="breadcrumb">Mayo 2026 · Fray</span>
    <span class="slide-num">01</span>
  </div>
</div>
```

### Blockquote

Cita destacada con barra verde a la izquierda:

```markdown
> "En Yucatán los apellidos importan más que las industrias."
```

- Fraunces 40px light
- Border-left 2px verde
- Italic, color `--lcg-dark`

---

## Cómo convertir un `.md` del proyecto a documento LCG

### Opción A — Pandoc (recomendado, rápido)

Instala Pandoc y wkhtmltopdf una vez:

```bash
# macOS
brew install pandoc wkhtmltopdf

# Linux
sudo apt install pandoc wkhtmltopdf

# Windows: descarga desde pandoc.org y wkhtmltopdf.org
```

Desde la raíz del proyecto, para convertir cualquier `.md` a HTML estilizado:

```bash
pandoc estados/05_yucatan/03_familias_empresariales.md \
  -o output/yucatan_familias.html \
  --standalone \
  --template=styles/template.html \
  --css=lcg.css \
  --metadata title="Familias Empresariales · Yucatán" \
  --metadata date="$(date +'%Y-%m-%d')"
```

Para generar PDF:

```bash
pandoc estados/05_yucatan/03_familias_empresariales.md \
  -o output/yucatan_familias.pdf \
  --standalone \
  --template=styles/template.html \
  --css=styles/lcg.css \
  --pdf-engine=wkhtmltopdf \
  --metadata title="Familias Empresariales · Yucatán"
```

### Opción B — Script de batch (todos los estados)

```bash
# Script: bin/build_documents.sh
mkdir -p output

for estado_dir in estados/*/; do
  estado=$(basename $estado_dir)
  for md in $estado_dir/0*.md; do
    nombre=$(basename $md .md)
    out_html="output/${estado}_${nombre}.html"
    pandoc "$md" -o "$out_html" \
      --standalone \
      --template=styles/template.html \
      --css=lcg.css \
      --metadata title="${estado} · ${nombre}"
    echo "✓ $out_html"
  done
done
```

### Opción C — Reveal.js (para presentaciones)

Para convertir un `.md` con headings en una presentación de diapositivas estilo LCG, usa el preset Reveal.js de Pandoc:

```bash
pandoc estados/05_yucatan/08_sintesis.md \
  -o output/yucatan_sintesis_slides.html \
  --slide-level=2 \
  -t revealjs \
  -V theme=white \
  -V revealjs-url=https://unpkg.com/reveal.js@5 \
  --css=styles/lcg.css \
  --css=styles/lcg-revealjs-overrides.css
```

*(El override de Reveal queda como tarea posterior cuando se quiera hacer presentaciones formales.)*

---

## Convenciones que los `.md` deben respetar

Para que el output visual sea limpio al renderizar, los `.md` del proyecto siguen estas convenciones:

### 1. Un solo H1 por archivo
El H1 es el título del documento. No usar múltiples H1.

```markdown
# Familias empresariales — Yucatán       ← solo uno

## Familia Vales                          ← H2 para secciones mayores
### Origen del patrimonio                 ← H3 para subsecciones
```

### 2. Cursiva para acentos clave
Cuando quieras destacar un nombre, concepto o número, usa `*énfasis*` o `_énfasis_`. Al renderizar quedará en cursiva verde estilo LCG.

```markdown
La *familia Vales* concentra el control accionario del Grupo Vales,
con una facturación estimada en *$3,200 MDP* anuales.
```

### 3. Tablas para datos comparables
Donde haya 2+ datos paralelos, usa tabla en lugar de bullet list.

```markdown
| Familia | Sector primario | Generación actual |
|---|---|---|
| Vales | Banca, retail | 3ª |
| Ponce | Pesca, construcción | 2ª |
```

### 4. Blockquotes para insights
Frases que quieres que sobresalgan visualmente.

```markdown
> El poder económico de Yucatán no se reparte: se hereda.
```

### 5. Encabezados de meta con H4
Para etiquetas tipo "INSIGHT", "CONTEXTO", "FUENTES" — H4 que se renderiza como eyebrow verde.

```markdown
#### Insight clave
Texto del insight...

#### Fuentes consultadas
- ...
```

### 6. Separadores horizontales para cambios de sección dentro de un mismo archivo
Tres guiones `---` se renderizan como línea divisoria sutil.

---

## Inspiración / referencias

El sistema sigue principios de:
- **The Economist** — uppercase eyebrows con letter-spacing positivo, sans serif para body
- **The New York Times opinion** — Fraunces para titulares editoriales, line-height comprimido
- **MIT Press** — tipografía generosa, márgenes amplios, énfasis quirúrgico
- **Bain Insights / McKinsey Quarterly** — paleta sobria, tablas sin zebra, cards sin sombra

---

## Resumen ejecutivo

| Aspecto | Decisión |
|---|---|
| Fondo principal | Crema `#F2EEE8` — nunca blanco |
| Tipografía display | Fraunces light (200-400) |
| Tipografía UI | Manrope (400-700) |
| Acento de color | Verde LCG `#03B585` |
| Cursiva verde | `<em>` dentro de titulares |
| Tracking de titulares | -0.03em |
| Tracking de meta | +0.16em uppercase |
| Cards | Sin sombra, border-radius 0 o 4px |
| Tablas | Sin zebra, border-bottom sutil |
| Pills | border-radius 999px |
| Padding de frame | 80px 100px |
