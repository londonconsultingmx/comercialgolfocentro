# Prompt 01 — Panorama económico del estado

## Objetivo
Generar el archivo `estados/<estado>/01_panorama_economico.md` con un panorama económico profundo y actualizado del estado.

## Instrucciones para Claude Code

Investiga y produce un análisis que responda:

### 1. Indicadores económicos clave
- PIB estatal (último dato INEGI) y posición en el ranking nacional
- Crecimiento PIB últimos 3 años
- PIB per cápita
- Población económicamente activa
- Tasa de informalidad
- Salario medio formal (IMSS)
- Inversión Extranjera Directa últimos 3 años (Secretaría de Economía)
- Exportaciones del estado (si dato disponible)

### 2. Composición sectorial del PIB
Distribución porcentual del PIB estatal por gran sector (primario, secundario, terciario) y sub-sectores dominantes. Tabla.

### 3. Geografía económica del estado
- Ciudades principales (top 3-5) y su rol económico
- Polos industriales o turísticos relevantes
- Conectividad: aeropuertos, puertos, red carretera, ferroviaria
- Frontera (si aplica) y cruces relevantes

### 4. Contexto reciente (últimos 12-24 meses)
- Anuncios de inversión grandes (>$100M USD)
- Proyectos federales / estatales relevantes (ej. Tren Maya, refinería Dos Bocas, polos del bienestar, IMMEX)
- Cambios regulatorios o de gobierno con impacto económico
- Nearshoring: ¿está pegando aquí? ¿qué empresas internacionales han llegado o anunciado?

### 5. Posicionamiento estratégico nacional
¿Qué rol juega este estado en la economía nacional? ¿Cuál es su ventaja comparativa? ¿Cuáles sus debilidades estructurales?

### 6. Riesgos y vulnerabilidades
- Concentración sectorial
- Seguridad pública (si afecta operaciones empresariales)
- Dependencia de un sector o cliente único
- Cuestiones laborales o sindicales relevantes

## Formato del output

- Markdown
- Mínimo 800 palabras, máximo 2,000
- Tablas siempre que ayuden a comparar (PIB por sector, top ciudades, inversiones recientes)
- Cada cifra con **fuente y fecha** en línea o nota al pie
- Sección final: **"Fuentes consultadas"** con URLs


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
- INEGI (banco de información económica, Censos Económicos, ENOE)
- Secretaría de Economía (datos IED)
- Banxico
- Gobierno del estado (informes, planes de desarrollo)
- IMSS (puestos de trabajo)
- ProMéxico / Invest in Mexico (si todavía existe)
- KPMG / EY / Deloitte (reportes regionales)
- Bancomer Research, Banamex Estudios Económicos
- Prensa: El Economista, El Financiero, Expansión, Forbes México, Bloomberg Línea
- Reportes de IMCO (Índice de Competitividad Estatal)

## No hagas
- No inventes cifras. Si no encuentras el dato, dilo.
- No copies bloques largos de fuentes (resume con tus palabras).
- No incluyas recomendaciones de outreach ni recomendaciones para LCG en este archivo (es panorama económico, neutro).
