# Estudio del estado: Tamaulipas

## Instrucciones para Claude Code

Eres responsable de generar el estudio completo del estado de **Tamaulipas**. Esto significa producir 8 archivos en esta carpeta (`estados/07_tamaulipas/`), ejecutando uno tras otro los prompts genéricos correspondientes y aplicándolos al contexto de **Tamaulipas**.

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

### Contexto pre-cargado de Tamaulipas

Las pistas siguientes son **puntos de partida** que conocemos de antemano. Verifica cada una con fuentes públicas antes de incluirla en los archivos finales. NO copies estas listas directamente — son orientación inicial. Investiga, valida, expande y corrige.

#### Sectores clave esperados
- Manufactura / maquila de exportación (Reynosa, Matamoros, Nuevo Laredo)
- Petróleo y energía (Tampico-Madero, costa)
- Logística fronteriza (Nuevo Laredo cruce #1)
- Petroquímica (Altamira)
- Agroindustria (sorgo, cítricos, ganado)
- Pesca y mariscos

#### Pistas de familias empresariales relevantes
- Familia Bichara (Bichara = construcción y comercio)
- Familia Cantú (varios)
- Familia Bracho
- Familia Loyo (presencia)
- Familia Yarrington (vinculaciones políticas)
- Familia Garza (presencia regional)

> ⚠️ Estas son hipótesis iniciales. Verifica que cada familia: (a) realmente existe, (b) sigue activa empresarialmente, (c) tiene relevancia económica suficiente para incluirse. Agrega familias adicionales que descubras y elimina las que ya no apliquen.

#### Pistas de grupos / empresas relevantes
- RHEEM Manufacturing Company
- MEDLINE (planta Reynosa)
- Stoneridge
- Delphi / Aptiv (varias plantas)
- Vitro (Tampico)
- Indelpro (Altamira)
- Mexichem / Orbia (Altamira)
- GE (varias plantas frontera)
- API Altamira / Tampico
- Pemex Logística (terminales)

#### Cámaras y asociaciones esperadas
- CAINTRA Tamaulipas
- INDEX Tamaulipas (Reynosa, Matamoros, Nuevo Laredo)
- COPARMEX Tamaulipas
- CCE Tamaulipas
- API Altamira
- Cámara de Comercio Tampico
- Cluster Manufactura Frontera Norte

### Para `07_empresas_top_30.md`

Cruza tres fuentes para identificar las **~30 empresas más relevantes del estado** (no son las "Tier A", son simplemente las que el estado considera importantes):

1. **Ranking Expansión 500** (`data/expansion/LCG_500_Empresas_Expansion_2025.csv`) — empresas cuya sede o operación principal sea Tamaulipas
2. **CRM HubSpot** (`data/crm/hubspot_empresas_AAA_AA.csv`) — filtra por `Estado de la República` == "Tamaulipas"
3. **Tu investigación de los archivos 02-04** — grupos y empresas que identificaste de fuentes públicas

Genera una tabla unificada:

| # | Empresa | Sector | Tamaño (empleados / ventas) | Origen del capital | Sede en el estado | En Expansión 500 (rank) | En CRM LCG | Owner LCG | Etapa | Notas |
|---|---------|--------|----------------------------|--------------------|--------------------|-------------------------|------------|-----------|-------|-------|

Después de la tabla, escribe **un párrafo breve por cada una de las top 10** explicando por qué importa.

### Para `08_sintesis.md`

Conclusión ejecutiva del estudio (mínimo 1,000 palabras), con:

1. **La narrativa económica del estado en un párrafo** — el "elevator pitch" de qué es Tamaulipas hoy
2. **Concentración del poder** — ¿pocas familias dominan? ¿hay competencia interna?
3. **Sectores donde se generará valor en los próximos 5 años**
4. **Patrones de cobertura del CRM de LCG** — análisis breve cruzando los hallazgos con `data/crm/`
5. **5 insights clave** que Fray debería tener en mente sobre Tamaulipas
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
> Ejecuta estados/07_tamaulipas/prompt.md completo, generando los 8 archivos y actualizando el README del estado.
```

O paso a paso, archivo por archivo:

```bash
> Ejecuta el paso 1 de estados/07_tamaulipas/prompt.md (panorama económico).
> (revisar el resultado, ajustar)
> Ejecuta el paso 2 (grupos empresariales).
> ... etc.
```
