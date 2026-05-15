# Estudio del estado: Ciudad de México

## Instrucciones para Claude Code

Eres responsable de generar el estudio completo del estado de **Ciudad de México**. Esto significa producir 8 archivos en esta carpeta (`estados/01_cdmx/`), ejecutando uno tras otro los prompts genéricos correspondientes y aplicándolos al contexto de **Ciudad de México**.

### Secuencia obligatoria

1. **`01_panorama_economico.md`** — usa `prompts/01_panorama_economico_estado/prompt.md`
2. **`02_grupos_empresariales.md`** — usa `prompts/02_grupos_empresariales_estado/prompt.md`
3. **`03_familias_empresariales.md`** — usa `prompts/03_familias_empresariales_estado/prompt.md`
4. **`04_sectores_clave.md`** — usa `prompts/04_sectores_clave_estado/prompt.md`
5. **`05_camaras_y_clusters.md`** — usa `prompts/05_camaras_clusters_estado/prompt.md`
6. **`06_ecosistema_decisores.md`** — usa `prompts/06_ecosistema_decisores_estado/prompt.md`
7. **`07_empresas_top_30.md`** — ver instrucciones específicas abajo
8. **`08_sintesis.md`** — ver instrucciones específicas abajo
9. **Actualiza `00_README.md`** con los hallazgos principales (usa `plantillas/TEMPLATE_ESTADO_README.md`).

### Contexto pre-cargado de Ciudad de México

Las pistas siguientes son **puntos de partida** que conocemos de antemano. Verifica cada una con fuentes públicas antes de incluirla en los archivos finales. NO copies estas listas directamente — son orientación inicial. Investiga, valida, expande y corrige.

#### Sectores clave esperados
- Servicios financieros (todo el sistema bancario nacional)
- Holdings corporativos (sede nacional de la mayoría de los grupos del país)
- Telecomunicaciones (América Móvil, Televisa)
- Retail y consumo (sedes corporativas de Liverpool, Soriana, Walmart México)
- Bienes raíces y construcción
- Medios y entretenimiento
- Servicios profesionales (consultoría, legal, big four)

#### Pistas de familias empresariales relevantes
- Slim (Carso, América Móvil, Inbursa, Sanborns)
- Salinas Pliego (Grupo Salinas, Banco Azteca, TV Azteca, Elektra)
- Bailleres / Bailleres González (Grupo BAL, Peñoles, GNP, Palacio de Hierro, ITAM)
- Larrea Mota Velasco (Grupo México)
- Azcárraga (Televisa, Posadas)
- Servitje (Grupo Bimbo)
- Alemán (CIE, Interjet histórico)
- González Nova (Comercial Mexicana → Soriana)
- Hernández Pons (Herdez)
- Vázquez Raña (familia, varios negocios)
- Robinson Bours (Bachoco) — aunque originarios de Sonora, sede CDMX

> ⚠️ Estas son hipótesis iniciales. Verifica que cada familia: (a) realmente existe, (b) sigue activa empresarialmente, (c) tiene relevancia económica suficiente para incluirse. Agrega familias adicionales que descubras y elimina las que ya no apliquen.

#### Pistas de grupos / empresas relevantes
- Grupo Carso, América Móvil, Inbursa, Sanborns
- Grupo BAL (Peñoles, GNP, Palacio de Hierro, Profuturo)
- Grupo México (Larrea)
- FEMSA (sede CDMX para algunas filiales aunque Monterrey es matriz)
- Grupo Bimbo
- Cemex (sede operativa CDMX y Monterrey)
- Televisa
- Grupo Salinas
- Liverpool
- Soriana / Walmart México
- Kimberly-Clark de México
- IEnova / Sempra Infraestructura
- BBVA, Banamex, Santander, Banorte (sedes nacionales)

#### Cámaras y asociaciones esperadas
- CCE (Consejo Coordinador Empresarial) — sede nacional
- CMN (Consejo Mexicano de Negocios)
- COPARMEX CDMX
- Concamin
- Concanaco-Servytur
- ABM (Asociación de Bancos de México)
- AMIB (intermediarios bursátiles)
- Bolsa Mexicana de Valores
- AMITI / CANIETI (tecnología)
- IMEF Grupo CDMX

### Para `07_empresas_top_30.md`

Cruza tres fuentes para identificar las **~30 empresas más relevantes del estado** (no son las "Tier A", son simplemente las que el estado considera importantes):

1. **Ranking Expansión 500** (`data/expansion/LCG_500_Empresas_Expansion_2025.csv`) — empresas cuya sede o operación principal sea Ciudad de México
2. **CRM HubSpot** (`data/crm/hubspot_empresas_AAA_AA.csv`) — filtra por `Estado de la República` == "CDMX"
3. **Tu investigación de los archivos 02-04** — grupos y empresas que identificaste de fuentes públicas

Genera una tabla unificada:

| # | Empresa | Sector | Tamaño (empleados / ventas) | Origen del capital | Sede en el estado | En Expansión 500 (rank) | En CRM LCG | Owner LCG | Etapa | Notas |
|---|---------|--------|----------------------------|--------------------|--------------------|-------------------------|------------|-----------|-------|-------|

Después de la tabla, escribe **un párrafo breve por cada una de las top 10** explicando por qué importa.

### Para `08_sintesis.md`

Conclusión ejecutiva del estudio (mínimo 1,000 palabras), con:

1. **La narrativa económica del estado en un párrafo** — el "elevator pitch" de qué es Ciudad de México hoy
2. **Concentración del poder** — ¿pocas familias dominan? ¿hay competencia interna?
3. **Sectores donde se generará valor en los próximos 5 años**
4. **Patrones de cobertura del CRM de LCG** — análisis breve cruzando los hallazgos con `data/crm/`
5. **5 insights clave** que Fray debería tener en mente sobre Ciudad de México
6. **Preguntas abiertas** — qué información faltaría para tener un mapa completo (orientado a futuras reuniones de descubrimiento)

### Reglas de calidad

- Cada archivo debe cumplir las exigencias del prompt genérico correspondiente.
- Cita fuentes con URL y fecha.
- Si un dato no está disponible, dilo. No inventes.
- No diseñes plan de outreach.
- No clasifiques empresas en Tier A/B/C.
- Idioma: español de México.

### Cómo invocar este estudio en Claude Code

```bash
# Una vez dentro del proyecto con Claude Code corriendo:
> Ejecuta estados/01_cdmx/prompt.md completo, generando los 8 archivos y actualizando el README del estado.
```

O paso a paso, archivo por archivo:

```bash
> Ejecuta el paso 1 de estados/01_cdmx/prompt.md (panorama económico).
> (revisar el resultado, ajustar)
> Ejecuta el paso 2 (grupos empresariales).
> ... etc.
```
