# Expansión 500

## `LCG_500_Empresas_Expansion_2025.csv`

- **Fuente:** Revista Expansión, ranking "Las 500 Empresas Más Importantes de México", edición 2025 (datos 2024)
- **URL fuente:** https://500empresas.expansion.mx
- **Estructura del archivo:**
  - Filas 1-3: metadatos (saltar con `skiprows=4` al leer)
  - Fila 5 (header): `Rank`, `Empresa`, `Sector`, `País`, `Ventas (MDP)`, `Utilidad Neta (MDP)`, `Utilidad de Operación (MDP)`, `Activo Total (MDP)`, `Pasivo Total (MDP)`, `Empleados`, `ROE (%)`, `Datos gobernanza`, `Ranking Ganado`
  - Filas 6+: 500 empresas

**Cómo cargarlo:**

```python
import pandas as pd
exp = pd.read_csv('data/expansion/LCG_500_Empresas_Expansion_2025.csv', skiprows=4)
```

## Limitaciones

- **No incluye el estado/ciudad de la sede** de cada empresa. Hay que inferirlo o cruzarlo con otras fuentes.
- **Ventas en MDP, columnas como strings con comas** (necesitan limpieza para análisis numérico).
- **No incluye nombres de ejecutivos** ni estructura accionaria.

## Cruce con estados

Para identificar empresas Expansión 500 con sede en cada estado, lo más confiable es:

1. Cruzar por nombre normalizado contra `data/crm/hubspot_empresas_AAA_AA.csv` (que sí trae `Estado de la República`)
2. Para las que no estén en CRM, consultar el sitio web corporativo o LinkedIn de la empresa
3. Validar con la base de la BMV o SEC si cotiza

## Sectores más representados en Expansión 500

- Servicios financieros (68)
- Alimentos y bebidas (33)
- Seguros y fianzas (33)
- Automotriz y autopartes (27)
- Armadora (21)
- Holding (20)
- Minería (18)
- Comercio autoservicio (16)
- Logística y transporte (15)
- Química farmacéutica (14)
- Química y petroquímica (12)
- Telecomunicaciones (11)
- Siderurgia y metalurgia (11)
- Productos de consumo (11)
- Construcción (11)
