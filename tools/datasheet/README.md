# Datasheet build

The datasheet source is maintained in Markdown under `chapters/`. Document
metadata and chapter order are defined in `book.yml`.

## Local build

Requirements:

- Pandoc
- WeasyPrint

Run from the repository root:

```bash
./tools/datasheet/build.sh
```

Generated files are written to `build/datasheet/`:

```text
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.md
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.docx
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.html
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.pdf
```
