# Metodología del Estudio

## Filosofía

Este es un **estudio de mercado de zona Sur-Centro-Golfo (12 estados)** orientado a entender, antes de actuar, el ecosistema empresarial de cada estado. El plan comercial se decide **después**, con la información en mano.

## Nivel de exigencia

- **Calidad consultoría tier-1** (McKinsey / Bain / BCG)
- **Honestidad sobre la incertidumbre**: cuando la información no está, decirlo, no inventarla
- **Fuentes citadas siempre**: URL y fecha de consulta

## Niveles de análisis

```
   ESTADO (12)
       │
       ├── Panorama económico
       ├── Grupos empresariales
       ├── Familias del poder económico
       ├── Sectores clave
       ├── Cámaras y clusters
       ├── Ecosistema de decisores
       ├── Top 30 empresas (cruce con CRM)
       └── Síntesis ejecutiva
              │
              ▼
   EMPRESA (seleccionadas)
       │
       └── Ficha profunda (formato PI Group, 9 secciones)
              │
              ▼
   DECISOR (top identificados)
       │
       └── Perfil individual (one-pager)
```

## Triangulación de fuentes

Cada dato relevante debe sustentarse en al menos una fuente verificable. Cuando hay conflicto entre fuentes, se documenta la divergencia.

### Tipos de fuentes utilizadas

**Públicas oficiales:**
- INEGI (Censos Económicos, ENOE, banco de información económica)
- Secretaría de Economía (IED, IMMEX)
- IMSS (empleo formal)
- BMV / SEC (empresas cotizadas)
- Banxico
- Gobiernos estatales
- IMCO (Índice de Competitividad Estatal)
- DATATUR / SECTUR (turismo)

**Privadas / corporativas:**
- Sitios web corporativos
- Reportes anuales de empresas
- LinkedIn (empresa y ejecutivos)

**Prensa especializada:**
- El Financiero, El Economista, Reforma, Expansión, Forbes México, Bloomberg Línea, Mexico Business News, Reuters

**Consultoras y rankings:**
- Ranking Expansión 500
- Reportes KPMG, EY, Deloitte, PwC
- Forbes Millonarios

**Internas:**
- HubSpot CRM de LCG MX (CSVs en `data/crm/`)

## Convenciones de notación

| Notación | Significado |
|---|---|
| `[DATO NO DISPONIBLE]` | El dato existe pero no fue accesible públicamente |
| `[NO IDENTIFICADO EN FUENTES PÚBLICAS]` | Búsqueda sin éxito en fuentes públicas |
| `[A VERIFICAR EN REUNIÓN]` | Pendiente para validación directa |
| `[ESTIMACIÓN]` | Dato no oficial, calculado con base en proxies |
| `[INFERIDO]` | Conclusión razonada de Claude basada en información parcial |
| `[Trascendido en prensa: ...]` | Información de prensa que la empresa no ha confirmado oficialmente |

## Sensibilidad y datos personales

- **No se publican correos, celulares o direcciones particulares** aunque aparezcan en el CRM.
- **No se inventan parentescos, edades, montos de patrimonio o conflictos familiares.**
- Información sobre familias y decisores se limita a lo público y documentable.

## Actualización

El proyecto está pensado para ser **vivo**. Cada archivo es independiente. Al obtener información nueva (ej. cambio de CEO de una empresa, anuncio de M&A, nueva familia en escena), se abre el archivo correspondiente, se actualiza, y se anota la fecha de revisión.

Recomendado: `git init` en el directorio del proyecto y commits frecuentes.
