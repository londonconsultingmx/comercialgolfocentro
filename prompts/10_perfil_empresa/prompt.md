# Prompt 10 — Investigación profunda de empresa (formato PI Group / TAFER)

## Objetivo
Generar las **fichas de investigación profunda de empresa** en `empresas/<id_empresa>/investigacion.md`, replicando exactamente el formato de los casos previos PI Group y Grupo TAFER & Villa Group.

## Instrucciones para Claude Code

Sigue el template completo en `plantillas/TEMPLATE_EMPRESA.md`.

### Calidad esperada
- Nivel: **investigación de cuenta de consultoría tier-1**. Léete `PI_Group_Investigacion_LCG.docx` (en el proyecto raíz de Claude del usuario) si necesitas referencia de profundidad.
- Mínimo **1,500 palabras**, ideal 2,500-4,000.
- 9 secciones obligatorias (ver template).
- Tablas en cada sección donde aporten claridad.

### Fuentes a consultar (por orden de prioridad)
1. **Sitio web corporativo** (sección About / Inversionistas / Sustentabilidad)
2. **LinkedIn** (página de empresa + perfiles de ejecutivos clave)
3. **BMV / SEC EDGAR** si cotiza
4. **Ranking Expansión 500** (en `data/expansion/`) si aplica
5. **`data/crm/hubspot_empresas_AAA_AA.csv`** filtrando por la empresa investigada — extrae propietario, etapa, contactos asociados, etc.
6. **`data/crm/hubspot_contactos.csv`** filtrando por la empresa — contactos en CRM
7. **Prensa**: El Financiero, El Economista, Expansión, Forbes México, Bloomberg Línea, Reuters
8. **Cámaras del sector** (donde la empresa esté afiliada)
9. **Reportes de consultoras** (KPMG, EY, Deloitte, PwC) si han hablado de la empresa o el sector
10. **Bases comerciales** (ZoomInfo / RocketReach / Apollo) para ejecutivos — solo si necesario y nunca extraigas correos para publicar

### Estructura del archivo (resumen — ver template para detalle)

1. **Perfil corporativo** — Razón social, fundación, sede, modelo de negocio, certificaciones
2. **Estructura del grupo / líneas de negocio** — Holding, subsidiarias, divisiones
3. **División principal de operación** — Detalle del core business
4. **Otras divisiones / servicios** — Líneas secundarias
5. **Posicionamiento estratégico y contexto de mercado** — Tendencias, factores externos
6. **Gobierno corporativo y liderazgo** — Directivos identificados con cargos y formación
7. **Certificaciones y reconocimientos clave**
8. **Oportunidades para la firma de consultoría** — 5-7 áreas donde LCG podría aportar valor (sin escribir pitch — solo "qué se podría hacer")
9. **Fuentes y notas metodológicas**

### Reglas específicas

- **Cuando un dato no esté disponible**, marca claramente:
  - `[DATO NO DISPONIBLE — empresa privada]`
  - `[NO IDENTIFICADO EN FUENTES PÚBLICAS]`
  - `[A VERIFICAR EN REUNIÓN DE DESCUBRIMIENTO]`
- **No inventes apellidos, cargos, montos ni relaciones**.
- **No publiques correos ni teléfonos** aunque estén en el CRM. Si menciones contactos identificados, usa solo nombre y cargo.
- **Identifica oportunidades de consultoría LCG sin escribir pitch**. Solo describe qué se podría hacer y por qué (ej. "Empresa familiar de 30+ años sin gobierno corporativo formal — oportunidad de profesionalización"). El pitch lo redacta Fray después.

### Sub-archivo: resumen ejecutivo

Adicional a `investigacion.md`, genera `resumen_ejecutivo.md` con la misma información en formato **one-pager** (máximo 600 palabras):
- 3 párrafos de contexto
- Tabla resumida (sede, sector, tamaño, modelo)
- 3-5 bullets de "qué saber antes de la primera reunión"
- 3 oportunidades de consultoría top

## Cuándo activar este prompt

Solo cuando Fray seleccione explícitamente una empresa para investigar. Por ejemplo:

```
> Investiga a profundidad empresas/015_softys_de_mexico/ siguiendo prompts/10_perfil_empresa/prompt.md
```

No generes fichas de empresas a menos que Fray las pida una por una o por lotes específicos.

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
