#!/bin/bash
# ============================================================
# build_documents.sh — Convierte los .md del proyecto a HTML/PDF estilizados
# ============================================================
#
# Uso:
#   ./bin/build_documents.sh              # genera todo en output/
#   ./bin/build_documents.sh estados/05_yucatan  # solo un estado
#   ./bin/build_documents.sh --pdf        # genera también PDFs
#
# Requiere: pandoc (brew install pandoc / apt install pandoc)
# Para PDFs: wkhtmltopdf o weasyprint
# ============================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

OUTPUT_DIR="output"
TEMPLATE="styles/template.html"
CSS_PATH="lcg.css"   # ruta relativa al output (los HTML quedan al lado de la copia del CSS)

mkdir -p "$OUTPUT_DIR"
cp styles/lcg.css "$OUTPUT_DIR/lcg.css"

# Detectar si se pidió un path específico
TARGET=""
GEN_PDF=false
for arg in "$@"; do
  case "$arg" in
    --pdf) GEN_PDF=true ;;
    *) TARGET="$arg" ;;
  esac
done

if ! command -v pandoc &> /dev/null; then
  echo "✖ Pandoc no encontrado. Instala con: brew install pandoc (macOS) o apt install pandoc (Linux)"
  exit 1
fi

# Función de conversión
convert_md() {
  local md_path="$1"
  local rel_path="${md_path#./}"
  local out_name="${rel_path//\//_}"
  out_name="${out_name%.md}.html"
  local out_path="$OUTPUT_DIR/$out_name"
  local title=$(basename "$md_path" .md | tr '_' ' ')
  local fecha=$(date +'%d %b %Y')

  pandoc "$md_path" \
    -o "$out_path" \
    --standalone \
    --template="$TEMPLATE" \
    --css="$CSS_PATH" \
    --metadata title="$title" \
    --metadata date="$fecha" \
    --from markdown \
    --to html5 \
    2>/dev/null && echo "  ✓ $out_path"

  if [ "$GEN_PDF" = true ]; then
    local pdf_path="${out_path%.html}.pdf"
    if command -v weasyprint &> /dev/null; then
      weasyprint "$out_path" "$pdf_path" 2>/dev/null && echo "    ✓ $pdf_path"
    elif command -v wkhtmltopdf &> /dev/null; then
      wkhtmltopdf --quiet --enable-local-file-access \
        --print-media-type "$out_path" "$pdf_path" && echo "    ✓ $pdf_path"
    else
      echo "    ⚠ Sin convertidor PDF (instala weasyprint o wkhtmltopdf)"
    fi
  fi
}

echo ""
echo "▸ Convirtiendo .md a HTML estilizado LCG..."
echo "  Output: $OUTPUT_DIR/"
echo ""

if [ -z "$TARGET" ]; then
  # Procesar todos los .md del proyecto
  echo "  Universo completo (estados + empresas + decisores + docs)"
  echo ""
  while IFS= read -r f; do
    convert_md "$f"
  done < <(find estados empresas decisores docs -name "*.md" -type f 2>/dev/null | sort)
else
  # Procesar un directorio o archivo específico
  if [ -d "$TARGET" ]; then
    echo "  Target: $TARGET/"
    echo ""
    while IFS= read -r f; do
      convert_md "$f"
    done < <(find "$TARGET" -name "*.md" -type f | sort)
  elif [ -f "$TARGET" ]; then
    echo "  Target: $TARGET"
    echo ""
    convert_md "$TARGET"
  else
    echo "✖ Target no encontrado: $TARGET"
    exit 1
  fi
fi

echo ""
echo "▸ Listo. Abre $OUTPUT_DIR/ en tu navegador."
echo ""
