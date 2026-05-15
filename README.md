# LCG Zona Sur-Centro — Inteligencia de Mercado

## Estudio de mercado profundo · 12 estados · Plataforma Claude Code

Investigación integral del ecosistema empresarial de los 12 estados de la zona comercial de Fray en LCG MX. Replica la metodología del proyecto previo `lcg-market-intelligence` (sector hotelero), adaptada a un eje **estado-céntrico** que cubre todos los sectores.

---

## Filosofía del proyecto

> **"Primero entender, después decidir."**

Este NO es un plan de outreach. Es un **estudio para entender el ecosistema empresarial estado por estado**. El plan comercial se construye después con esta información en mano.

Tres niveles de análisis:

1. **Estado** — Quién manda económicamente, qué sectores dominan, qué grupos y familias controlan el poder económico local.
2. **Empresa** — Fichas profundas de cuentas relevantes, estilo PI Group / TAFER.
3. **Decisor** — Perfiles individuales de personas clave (CEOs, dueños, CFOs).

---

## Cómo arrancar

### Pre-requisitos
- Claude Code instalado (`npm install -g @anthropic-ai/claude-code` o ver `https://claude.com/claude-code`)
- Cuenta Claude con acceso

### Inicio
```bash
# 1. Descomprime y entra al proyecto
unzip lcg-zona-sur-centro.zip
cd lcg-zona-sur-centro

# 2. Inicia Claude Code
claude

# 3. Claude lee CLAUDE.md automáticamente. Pídele:
> Lee CLAUDE.md y dame un resumen del proyecto.

# 4. Empieza por el primer estado:
> Lee estados/01_cdmx/prompt.md y ejecuta el estudio completo de CDMX.
#   Genera los 8 archivos siguiendo los prompts en /prompts/01..06/.
```

### Flujo recomendado

```
Estado 01 (CDMX) → revisar → ajustar → siguiente estado
        ↓
Estado 02 (EdoMex) → ...
        ↓
... (12 estados)
        ↓
Empresas seleccionadas → fichas profundas
        ↓
Decisores top → perfiles individuales
        ↓
Síntesis cross-estatal
```

---

## Estructura del proyecto

```
lcg-zona-sur-centro/
├── CLAUDE.md                # Cerebro: instrucciones para Claude Code
├── README.md                # Este archivo
├── bin/
│   └── build_documents.sh   # Convierte .md a HTML/PDF estilizado LCG
├── data/                    # CSVs del CRM + Expansión 500
├── estados/                 # 12 estudios de estado (eje principal)
├── empresas/                # Fichas profundas estilo PI Group
├── decisores/               # Perfiles individuales de personas clave
├── prompts/                 # Prompts reutilizables
├── plantillas/              # Templates de estado, empresa, decisor
├── styles/                  # Sistema visual LCG (CSS + template Pandoc)
└── docs/                    # Metodología, fuentes, glosario
```

Para detalle completo, ver `CLAUDE.md`.

---

## Sistema visual LCG

El proyecto incluye un sistema visual institucional completo en `styles/`:

- **Paleta:** verde institucional `#085E54`, verde LCG `#03B585`, mint, crema cálida (nunca blanco puro)
- **Tipografía:** Fraunces (serif, titulares) + Manrope (sans, body)
- **Componentes:** cards sin sombra, pills redondeados, tablas sin zebra, números display, blockquotes con barra verde

Cuando quieras convertir un `.md` del proyecto a HTML/PDF estilizado:

```bash
# Instala Pandoc una vez
brew install pandoc                                # macOS
sudo apt install pandoc                            # Linux

# Convierte un estado completo
./bin/build_documents.sh estados/05_yucatan

# Convierte todo el proyecto
./bin/build_documents.sh

# Genera también PDFs (requiere weasyprint o wkhtmltopdf)
./bin/build_documents.sh --pdf
```

Los HTML/PDF resultantes quedan en `output/` con la paleta y tipografía institucional aplicadas.

Ver `styles/SISTEMA_VISUAL.md` para la guía completa.

---

## Tip de uso

Cada estado tarda varias horas de investigación profunda. **No le pidas a Claude que haga los 12 estados de un tirón** — la calidad bajaría. Hazlo en bloques:

- Sesión 1: CDMX completo
- Sesión 2: Estado de México completo
- Sesión 3: Puebla completo
- ... etc.

Revisa, valida con tu conocimiento local, pide ajustes específicos, y avanza al siguiente. La estructura está pensada para soportar trabajo iterativo a lo largo de semanas.

---

## Mantenimiento

El proyecto está pensado para ser **vivo**:
- Cada archivo es independiente y editable.
- Cuando obtengas información nueva (ej. cambio de CEO en una empresa), abres el archivo, lo actualizas y commit.
- Recomendado: `git init` y commits frecuentes.

---

## Contacto

Owner del proyecto: **Fray** · Director de Operaciones · LCG MX
