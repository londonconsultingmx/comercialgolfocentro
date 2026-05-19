# Prompt 11 — Perfil individual de un decisor

## Objetivo
Generar perfiles individuales en `decisores/<apellido_nombre>/perfil.md` para personas clave identificadas en los estudios de estado.

## Cuándo activar
Solo a petición de Fray. Ej:

```
> Genera el perfil individual de decisores/azcarraga_jose_carlos/ siguiendo prompts/11_perfil_decisor/prompt.md
```

## Instrucciones para Claude Code

Sigue el template en `plantillas/TEMPLATE_DECISOR.md`.

### Estructura del archivo

```markdown
# <Nombre completo>

| Campo | Detalle |
|-------|---------|
| Rol principal | <cargo + empresa> |
| Otros roles | <consejos, presidencias, fundaciones> |
| Empresa(s) que controla / dirige | <listado> |
| Familia (si aplica) | <apellido y rama> |
| Edad aproximada | <si pública> |
| Lugar de nacimiento | <si público> |
| Residencia actual | <ciudad si pública> |
| LinkedIn | <URL pública> |

## 1. Trayectoria profesional
Narrativa cronológica de la carrera de la persona. Cada salto importante con su contexto.

## 2. Formación
- Licenciatura: <universidad, año si disponible>
- Posgrados / programas ejecutivos: <listado>
- Idiomas conocidos públicamente

## 3. Estilo de liderazgo
Inferido de:
- Entrevistas públicas
- Declaraciones en medios
- Decisiones empresariales conocidas
- Cómo lo describen en prensa

(Mantén lenguaje cauto: "se le describe como...", "ha declarado...")

## 4. Intereses y filantropía
- Causas que apoya públicamente
- Fundaciones donde participa
- Hobbies o pasiones documentadas en prensa
- Participación en deportes, arte, cultura

## 5. Red de relaciones públicas
- Otros decisores con los que coincide en consejos
- Cámaras donde participa
- Eventos a los que asiste regularmente
- Relaciones empresariales documentadas (joint ventures, M&A)

## 6. Señales recientes (últimos 12-18 meses)
- Declaraciones públicas relevantes
- Decisiones empresariales atribuibles
- Cambios de posición / cargo
- Reconocimientos recibidos
- Asistencia a foros internacionales

## 7. Notas para LCG
*(Sin redactar pitch — solo flags relevantes)*
- ¿Tiene relación previa con LCG según el CRM? (consultar `data/crm/hubspot_contactos.csv`)
- ¿Está en momento de transición / sucesión / profesionalización?
- ¿Hay temas en su agenda pública donde LCG haya hecho buen trabajo antes?
- ¿Tiene conexiones con clientes actuales o ex-clientes de LCG?

## 8. Fuentes consultadas
- URLs específicas
- Fechas de consulta
```

### Reglas estrictas

- **Solo información pública.** Nada de información privada, especulación, rumores no documentados, ni inferencias sobre vida personal/familiar más allá de lo público.
- **No publiques correos, celulares, direcciones particulares**.
- **No inventes**. Si una sección queda corta porque la información pública es escasa, déjala corta. No rellenes.
- **Lenguaje neutral**. No editorices estilos personales con calificativos cargados ("agresivo", "blando", "déspota"). Usa observaciones documentadas.
- **No clasifiques nivel de "abordabilidad"**. Solo descripción.


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

## Output
- Un archivo `.md` por persona, en su carpeta dentro de `decisores/`.
- 500-1,200 palabras.
- Nombre de carpeta en formato `<apellido_paterno>_<nombre>` en minúsculas, sin acentos, separado con guiones bajos. Ej: `azcarraga_jose_carlos/`.
