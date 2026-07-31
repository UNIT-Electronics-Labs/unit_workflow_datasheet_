#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOK_FILE="$PROJECT_DIR/datasheet/book.yml"
REFERENCE_DOC="$PROJECT_DIR/datasheet/reference-a4.docx"
OUTPUT_DIR="${1:-$PROJECT_DIR/build/datasheet}"
OUTPUT_BASENAME="unit_datasheet_v_1_0_0_devlab_multi_hub_shield"

for command_name in pandoc libreoffice; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Error: falta el comando requerido: $command_name" >&2
    exit 1
  fi
done

for required_file in "$BOOK_FILE" "$REFERENCE_DOC"; do
  if [[ ! -f "$required_file" ]]; then
    echo "Error: no se encontró: $required_file" >&2
    exit 1
  fi
done

mapfile -t CHAPTERS < <(
  awk '
    /^chapters:/ { in_chapters=1; next }
    in_chapters && /^  - / { sub(/^  - /, ""); print; next }
    in_chapters && !/^  - / { exit }
  ' "$BOOK_FILE"
)

if [[ "${#CHAPTERS[@]}" -eq 0 ]]; then
  echo "Error: book.yml no contiene capítulos." >&2
  exit 1
fi

CHAPTER_PATHS=()
for chapter in "${CHAPTERS[@]}"; do
  if [[ ! -f "$PROJECT_DIR/$chapter" ]]; then
    echo "Error: falta el capítulo: $chapter" >&2
    exit 1
  fi
  CHAPTER_PATHS+=("$PROJECT_DIR/$chapter")
done

while IFS= read -r asset; do
  if [[ ! -f "$PROJECT_DIR/$asset" ]]; then
    echo "Error: un capítulo referencia un recurso inexistente: $asset" >&2
    exit 1
  fi
done < <(
  grep -hEo '!\[[^]]*\]\([^)]*\)' "${CHAPTER_PATHS[@]}" |
    sed 's/^.*](//;s/)$//' |
    sort -u
)

mkdir -p "$OUTPUT_DIR"

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

CONTENTS_FILE="$TEMP_DIR/contents.md"
{
  printf '%s\n' \
    '```{=openxml}' \
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>' \
    '```' \
    '' \
    '## Contents' \
    ''

  awk '
    /^## / {
      text=$0
      sub(/^## /, "", text)
      gsub(/\*\*/, "", text)
      sub(/[[:space:]]+$/, "", text)
      print "- [" text "]{.toc-entry}"
    }
    /^### / {
      text=$0
      sub(/^### /, "", text)
      gsub(/\*\*/, "", text)
      sub(/[[:space:]]+$/, "", text)
      print "  - [" text "]{.toc-entry}"
    }
  ' "${CHAPTER_PATHS[@]}"

  printf '%s\n' \
    '' \
    '```{=openxml}' \
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>' \
    '```'
} >"$CONTENTS_FILE"

DOCUMENT_INPUTS=("$CONTENTS_FILE" "${CHAPTER_PATHS[@]}")

MARKDOWN_FILE="$OUTPUT_DIR/$OUTPUT_BASENAME.md"
DOCX_FILE="$OUTPUT_DIR/$OUTPUT_BASENAME.docx"
PDF_FILE="$OUTPUT_DIR/$OUTPUT_BASENAME.pdf"

pandoc \
  --from=markdown \
  --to=gfm \
  --metadata-file="$BOOK_FILE" \
  "${DOCUMENT_INPUTS[@]}" \
  --output="$MARKDOWN_FILE"

pandoc \
  --from=markdown \
  --to=docx \
  --standalone \
  --metadata-file="$BOOK_FILE" \
  --reference-doc="$REFERENCE_DOC" \
  --resource-path="$PROJECT_DIR" \
  "${DOCUMENT_INPUTS[@]}" \
  --output="$DOCX_FILE"

libreoffice \
  --headless \
  "-env:UserInstallation=file://$TEMP_DIR/libreoffice-profile" \
  --convert-to pdf \
  --outdir "$TEMP_DIR" \
  "$DOCX_FILE"

GENERATED_PDF="$TEMP_DIR/$OUTPUT_BASENAME.pdf"
if [[ ! -s "$GENERATED_PDF" ]]; then
  echo "Error: LibreOffice no generó el PDF." >&2
  exit 1
fi

install -m 0644 "$GENERATED_PDF" "$PDF_FILE"

echo "Datasheet construido:"
echo "  Markdown: $MARKDOWN_FILE"
echo "  DOCX:     $DOCX_FILE"
echo "  PDF:      $PDF_FILE"
