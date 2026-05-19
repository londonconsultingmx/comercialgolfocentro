# Prompt 04 — Sectores clave del estado

## Objetivo
Generar el archivo `estados/<estado>/04_sectores_clave.md` que identifique y analice los **sectores económicos dominantes** del estado, qué empresas lideran cada uno, y la dinámica competitiva.

## Instrucciones para Claude Code

### Selección de sectores
Identifica los **5-8 sectores más relevantes** del estado según:
1. Contribución al PIB estatal
2. Generación de empleo formal
3. Concentración de empresas grandes (AAA/AA del CRM, Expansión 500)
4. Importancia estratégica nacional (ej. petróleo en Tabasco, turismo en QR)

### Para cada sector, produce:

```markdown
## Sector: <Nombre>

### Panorama
- Importancia para la economía del estado (% PIB, empleo, exportaciones)
- Cadena de valor: ¿el estado tiene aguas arriba, abajo, o ensamblaje?
- Posición en el contexto nacional (¿es el estado #1 / #2 / #3 en este sector?)

### Empresas líderes en el estado
| Empresa | Subsector | Tamaño (empleados / ventas si público) | Origen del capital | Notas |
|---------|-----------|--------------------------------------|---------------------|-------|
| ... | ... | ... | Local / Nacional / Extranjero | ... |

Mínimo 5 empresas líderes por sector, hasta 15 en sectores fuertes.

### Cadena de valor local
- Proveedores relevantes
- Compradores institucionales (gobierno, otras empresas grandes)
- Servicios profesionales asociados (logística, manufactura por contrato, etc.)

### Tendencias del sector en el estado
- Crecimiento o decrecimiento últimos 3 años
- Tecnologías o modelos emergentes
- Presión competitiva (entrada de nuevos jugadores, consolidación, M&A)
- Regulación local / federal con impacto

### Pain points operativos típicos del sector
*(Sin recomendar outreach — solo describir qué duele en este sector hoy)*
- Ej. en manufactura automotriz: presión de tier-1s, transición eléctrica, escasez de talento técnico
- Ej. en agroindustria: clima, logística, certificaciones para exportación
- Ej. en hotelería: estacionalidad, rotación de personal, ESG

### Oportunidades para consultoría operativa
*(Identifica áreas donde una firma como LCG podría aportar valor — sin escribir pitch)*
- Optimización operativa
- Gobierno corporativo (especialmente si el sector tiene muchas empresas familiares)
- Transformación digital
- ESG / sostenibilidad
- Profesionalización de M&A

```

### Sección final del archivo

#### Síntesis sectorial del estado
- ¿Qué hace único a este estado en su mix sectorial?
- ¿Cuál es el sector "joya" donde el estado realmente sobresale?
- ¿Hay sectores en declive que están siendo reemplazados?
- ¿Hay sectores emergentes que en 5 años cambiarán el mapa?

## Formato
- Markdown
- Mínimo 1,200 palabras, idealmente 2,000-3,000
- Tablas por sector + narrativa
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
- INEGI (Censos Económicos por entidad)
- SE / IMMEX (manufactura)
- Secretaría de Economía estatal
- Cámaras sectoriales (Canacintra, CANIETI, AMIA, ANTAD, CMIC, ANIPAC, CONCAMIN, etc.)
- Reportes sectoriales de KPMG / EY / Deloitte / PwC
- DATATUR (turismo)
- SADER / SAGARPA (agro)
- CRE / SENER (energía)
- Prensa especializada del sector
- CSVs del CRM en `data/crm/` — los campos `Industria`, `Subindustria` y `Atributo de Industria` son tu mapa de qué sectores tiene cubiertos LCG

## No hagas
- No fuerces 8 sectores si el estado realmente tiene 4 dominantes (calidad sobre cantidad).
- No copies descripciones genéricas de sectores. Aterriza en este estado específicamente.
- No mezcles sectores en una sola narrativa (cada uno su sección).
