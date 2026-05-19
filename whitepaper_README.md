# Extractor Whitepaper.mx — Guía rápida

## Qué hace este script

Descarga los posts del tag **"Hoy"** de Whitepaper.mx del último año usando tu sesión autenticada. Por cada post genera:

- Un archivo `.md` legible con el contenido completo
- Un archivo `.json` con metadata (fecha, URL, título, subtítulo, conteo de palabras, etc.)
- Un índice maestro (`index.json` + `index.csv`) con todos los posts

---

## Setup (5 minutos)

### 1. Instala Python y dependencias

```bash
# Si no tienes Python 3.10+:
# macOS: brew install python
# Windows: descarga de python.org

pip install requests beautifulsoup4 markdownify python-dateutil
```

### 2. Obtén tu cookie de sesión de Substack

Esta es la parte importante. Tu cookie `substack.sid` es lo que autentica las peticiones como tú (suscriptor pagado).

**En Chrome / Edge / Brave:**

1. Abre [whitepaper.mx](https://www.whitepaper.mx) y asegúrate de estar logueado
2. Presiona `F12` (o `Cmd+Opt+I` en Mac) para abrir DevTools
3. Ve a la pestaña **Application** (en Firefox: **Storage**)
4. En el panel izquierdo expande **Cookies** → `https://www.whitepaper.mx`
5. Busca la cookie llamada `substack.sid`
6. Copia el **Value** (no el Name) — es un string largo tipo `s%3AAbCd1234...`

**Importante:** Esta cookie es equivalente a tu password. No la compartas ni la subas a Git.

### 3. Pega la cookie en el script

Abre `extract_whitepaper.py` y reemplaza:

```python
SUBSTACK_SESSION_COOKIE = "PEGA_AQUI_TU_COOKIE_substack.sid"
```

con el valor que copiaste.

### 4. Corre el script

```bash
python extract_whitepaper.py
```

Tarda **~5-8 minutos** para un año (~250 posts) con el throttling default de 1 segundo entre requests.

---

## Estructura de salida

```
output/
├── index.json          # Catálogo completo con metadata
├── index.csv           # Mismo catálogo, formato tabular (abre en Excel)
└── posts/
    ├── 2025-05-20_whitepaper-hoy-xyz.md     ← contenido legible
    ├── 2025-05-20_whitepaper-hoy-xyz.json   ← contenido + metadata
    ├── 2025-05-21_whitepaper-hoy-abc.md
    └── ...
```

---

## Cómo verificar que la autenticación funcionó

Después de correr, abre `output/index.csv` y revisa la columna `word_count`:

- **Posts gratuitos**: ~300-800 palabras (siempre completos)
- **Posts pagados con auth OK**: 1,500-4,000+ palabras ✅
- **Posts pagados sin auth**: ~50-150 palabras (solo la preview) ❌

Si todos tus posts pagados tienen ~100 palabras, la cookie no quedó bien. Vuelve a copiarla.

La columna `auth_ok` te marca explícitamente si el script logró traer contenido completo.

---

## Una vez que termine el script

Sube **a la conversación de Claude** uno de estos:

**Opción A (recomendada para empezar):** sube `output/index.json` — Claude ya puede arrancar el análisis de cobertura editorial, frecuencias, mapeo empresa-fecha sin necesidad de los cuerpos.

**Opción B (análisis profundo):** zippea la carpeta `output/posts/` y súbela. Claude extrae empresas mencionadas, montos, sectores, movimientos directivos, y arma las tablas estructuradas que pediste.

```bash
cd output && zip -r posts.zip posts/
```

---

## Troubleshooting

**`Host not in allowlist` / errores de red** → Estás detrás de VPN corporativa que bloquea. Apágala o corre desde casa.

**`HTTP 403` en todos los requests** → La cookie expiró o está mal copiada. Re-loguéate en whitepaper.mx y vuelve a copiarla.

**`no_body_found`** → Substack cambió el HTML. Avísame y ajusto el selector CSS en `fetch_post_body()`.

**Quiero más / menos de un año** → Edita `DATE_FROM` arriba en el script.

**Quiero que vaya más rápido** → Baja `DELAY_SECONDS` a 0.5. Cuidado con rate limits — si te empieza a fallar, vuelve a subirlo.

---

## Consideraciones legales

Este script descarga contenido al que **ya tienes acceso legítimo como suscriptor pagado**, para uso personal de análisis e inteligencia. Es equivalente a guardar páginas con "Save As" una por una, automatizado.

Lo que **no** debes hacer con la salida:
- Republicar el contenido íntegro en otro lado
- Compartir los archivos descargados con no-suscriptores
- Usar el material para crear un producto derivado que sustituya leer Whitepaper

Resúmenes ejecutivos, extracción de datos (empresas, montos, fechas), análisis agregado — todo eso sí.
