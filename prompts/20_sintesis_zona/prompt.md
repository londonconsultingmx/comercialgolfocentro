# Prompt 20 — Síntesis cross-estatal

## Objetivo
Una vez completados los 12 estudios de estado, generar `docs/sintesis_zona_sur_centro.md`: una síntesis transversal que conecte los hallazgos.

## Cuándo activar
Solo después de completar al menos 8-12 estados. Antes es prematuro.

## Instrucciones para Claude Code

Lee todos los archivos `00_README.md`, `06_ecosistema_decisores.md`, `07_empresas_top_30.md` y `08_sintesis.md` de los 12 estados.

### Estructura del documento

#### 1. Mapa de poder cross-estatal
- Familias o grupos cuya presencia abarca 3+ estados de la zona
- Empresas con sede en un estado pero operación significativa en otros 2+
- Cámaras o consejos con influencia multi-estatal

#### 2. Sectores cross-estatales
- Sectores que dominan en múltiples estados de la zona
- Cadenas de valor que se extienden por la zona (ej. agro de Veracruz → CDMX → exportación; turismo CDMX → Yucatán → Quintana Roo)
- Concentraciones de poder sectorial

#### 3. Decisores con influencia regional
- Personas que aparecen en mapas de decisores de múltiples estados
- "Conectores naturales" entre estados de la zona

#### 4. Ranking de oportunidad económica de la zona
Sin recomendar outreach, identifica patrones:
- ¿Qué estados tienen ecosistemas más maduros para servicios de consultoría?
- ¿Qué estados están en momento expansivo?
- ¿Qué estados tienen mayor concentración de empresas familiares grandes?

#### 5. Patrones de cobertura del CRM de LCG
Cruzando con `data/crm/`:
- ¿Dónde el CRM está más completo / fuerte?
- ¿Dónde hay huecos blancos sistemáticos?
- ¿Qué propietarios de LCG han concentrado actividad?

#### 6. Conclusiones para Fray
- 5-7 insights ejecutivos que solo se ven al mirar la zona como conjunto
- Sin recomendar plan de acción — solo observaciones

## Formato
- Markdown
- 2,000-4,000 palabras
- Tablas comparativas entre estados
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
