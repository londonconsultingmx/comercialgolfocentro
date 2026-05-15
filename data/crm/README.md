# Datos del CRM

Archivos sensibles. Listados en `.gitignore` — no se suben a repos públicos.

## Archivos

### `hubspot_empresas_AAA_AA.csv`
- **Origen:** HubSpot · LCG MX · export 2026-05-13
- **Filtro:** empresas clasificadas AAA o AA
- **Volumen:** ~2,640 empresas (todo México); 1,189 en los 12 estados objetivo
- **Universo efectivo del estudio:** 1,165 empresas (tras filtrar 24 marcadas como "No Cumple perfil")
- **Columnas clave:** `Nombre de la empresa`, `Clasificación` (AAA/AA), `Industria`, `Subindustria`, `Estado de la República`, `Zona`, `Etapa`, `Tipo de Cliente`, `Propietario del registro de empresa`, `Associated Contact`, `Associated Contact IDs`, `Última actividad`, `Fecha de creación`

**Definiciones:**
- **AAA** = empresas que facturan **más de USD $30M** anuales
- **AA** = empresas que facturan **entre USD $20M y $30M** anuales

**Filtros que debe aplicar Claude Code antes de cualquier análisis:**
1. Excluir empresas con `Etapa == "No Cumple perfil"` o `Tipo de Cliente == "No Cumple perfil"` (24 cuentas — no son parte del universo de trabajo).
2. Excluir empresas con `Etapa == "Cliente Anterior"` (33 cuentas — se trabajan en una iniciativa separada de reactivación de ex-clientes).

### `hubspot_contactos.csv`
- **Origen:** HubSpot · LCG MX
- **Volumen:** ~11,222 contactos
- **264 columnas** — la mayoría irrelevantes
- **Columnas relevantes para investigación:** `Nombre`, `Apellidos`, `Correo`, `Cargo`, `Puesto de trabajo`, `Nombre de la empresa`, `Estado de la República`, `Industria`, `URL de LinkedIn`, `Propietario del contacto`, `Etapa del ciclo de vida`, `Clasificación`, `Nivel de contacto`, `Última actividad`, `Estatus del Contacto`, `Hot Lead`, `Lead Scoring – GS`

⚠️ **Los correos electrónicos NO deben publicarse en archivos de investigación.** Sólo usa los CSVs como insumo para identificar si una persona/empresa está conocida por LCG; describe la relación pero no publiques contactos.

### `exclientes.csv`
- **Origen:** Vista de plan de acción de ex-clientes · HubSpot · LCG MX · subido 2026-05-14
- **Volumen:** 99 ex-clientes nacionales (todo México)
- **En la zona Sur-Centro-Golfo:** 36 ex-clientes (CDMX 19, Estado de México 5, Veracruz 4, Yucatán 2, Tamaulipas 2, Chiapas 1, Oaxaca 1, Tabasco 1, Hidalgo 1; sin presencia en Puebla, Quintana Roo, Guerrero)
- **Fuera de zona:** 60 ex-clientes (Nuevo León 27, Jalisco 9, otros 24) — no aplican a este proyecto
- **Columnas clave:** `ID HubSpot`, `Empresa`, `Plan de Acción`, `Prioridad` (0=no viable, 1=alta, 2=media, 3=de cero), `Asignado a`, `Estado`, `Industria`, `Tomador de Decisión / Dueño`, `Cargo`, `Email Decisor`, `# Contactos`, `# Deals`, `Última Interacción`, `Owner LCG`, `URL HubSpot`

**Cómo se usa este archivo:**
- La iniciativa de reactivación de ex-clientes es **paralela** a este estudio — ex-clientes NO son targets de priorización ni se profundizan en fichas de empresa.
- **PERO** su membresía en cámaras/clusters/networks del estado es relevante para entender el ecosistema local. Cruzar explícitamente en `05_camaras_y_clusters.md` de cada estado (con columna "Ex-cliente LCG" sí/no en las tablas).
- No publicar correos personales en archivos de investigación.

**Discrepancia conocida con `hubspot_empresas_AAA_AA.csv`:** el CRM AAA/AA reporta 33 "Cliente Anterior" en zona; `exclientes.csv` trae 36 en zona. Diferencia (+3) se explica probablemente por: (a) duplicados de ID HubSpot (ej. *Acosta Verde* / *GRUPO ACOSTA VERDE* comparten ID 18765886291; *Insultherm* / *GRUPO INSUL-THERM* comparten ID 18766002946), (b) ex-clientes que no son AAA/AA, (c) entradas "De cero" sin estado asignado (DIHASA, FEMSA, Reckit Beckinser).

**Encoding:** archivo limpiado de mojibake doble (UTF-8 → Latin-1 → UTF-8) en sesión de onboarding 2026-05-14. Quedó 100% legible.

---

### `INDICE_empresas_clasificadas.xlsx`
- **Origen:** Análisis previo elaborado en sesión Claude (mayo 2026)
- **Contenido:** workbook con tabs de Universo · Tier A · Tier B · Decisores · Cruce Expansión 500 · Cuentas Huérfanas
- **Uso en este proyecto:** índice rápido para identificar el universo de empresas AAA/AA en los 12 estados objetivo, sin tener que volver a cargar los CSVs en cada sesión.

**Nota importante:** Aunque el Excel ya tiene una clasificación Tier A/B/C basada en scoring, este proyecto **NO usa esa clasificación** para el estudio. El estudio debe ser exhaustivo del estado, no del CRM. El Excel sirve solo como referencia rápida cuando se quiera ver qué empresas del CRM existen en cada estado.

## Estados objetivo y cómo aparecen en los CSVs

| Estado | Cómo aparece en `Estado de la República` |
|---|---|
| Ciudad de México | `CDMX` |
| Estado de México | `Estado de México` |
| Veracruz | `Veracruz` |
| Puebla | `Puebla` |
| Yucatán | `Yucatán` |
| Quintana Roo | `Quintana Roo` |
| Tamaulipas | `Tamaulipas` |
| Tabasco | `Tabasco` |
| Hidalgo | `Hidalgo` |
| Chiapas | `Chiapas` |
| Guerrero | `Guerrero` |
| Oaxaca | `Oaxaca` |

## Conteos pre-calculados de cada estado

## Conteos pre-calculados de cada estado

Cifras del universo efectivo del estudio (1,165 empresas — sin "No Cumple perfil"). Los contactos se muestran sin filtrar por empresa.

| Estado | Empresas AAA/AA | Contactos |
|---|---|---|
| CDMX | 653 | 2,369 |
| Estado de México | 214 | 981 |
| Puebla | 69 | 317 |
| Quintana Roo | 56 | 224 |
| Veracruz | 54 | 334 |
| Tamaulipas | 43 | 206 |
| Yucatán | 35 | 164 |
| Hidalgo | 15 | 59 |
| Tabasco | 9 | 68 |
| Guerrero | 7 | 27 |
| Chiapas | 6 | 37 |
| Oaxaca | 4 | 23 |
| **TOTAL** | **1,165** | **4,809** |

**Notas:**
- CDMX + Estado de México concentran 867 empresas (74% del universo filtrado).
- 33 empresas adicionales tienen etapa "Cliente Anterior" (ex-clientes) y se trabajan en otra iniciativa — no aparecen en la tabla anterior.
- 24 empresas adicionales con etapa "No Cumple perfil" fueron excluidas — no son parte del universo de trabajo.

## Cómo usar los CSVs en investigación

### Pandas (recomendado para Claude Code)

```python
import pandas as pd

# Cargar empresas AAA/AA
emp = pd.read_csv('data/crm/hubspot_empresas_AAA_AA.csv')

# Aplicar filtros del universo efectivo (ANTES de cualquier análisis)
emp = emp[~emp['Etapa'].isin(['No Cumple perfil', 'Cliente Anterior'])]
emp = emp[~emp['Tipo de Cliente'].isin(['No Cumple perfil', 'Cliente Anterior'])]
# Universo resultante: 1,132 empresas (1,165 menos los 33 Cliente Anterior)

# Filtrar por estado
emp_yuc = emp[emp['Estado de la República'] == 'Yucatán']
print(emp_yuc[['Nombre de la empresa', 'Industria', 'Etapa', 'Clasificación', 'Propietario del registro de empresa']])

# Cargar contactos
con = pd.read_csv('data/crm/hubspot_contactos.csv', low_memory=False)
cols_clave = ['Nombre', 'Apellidos', 'Cargo', 'Nombre de la empresa',
              'Estado de la República', 'Industria', 'URL de LinkedIn',
              'Propietario del contacto', 'Etapa del ciclo de vida']
con_yuc = con[con['Estado de la República'] == 'Yucatán'][cols_clave]
```
