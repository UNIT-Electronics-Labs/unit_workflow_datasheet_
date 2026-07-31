# Product reference build

The product reference source is maintained in Markdown under `chapters/`. Document
metadata and chapter order are defined in `book.yml`.

## Local build

Requirements:

- Pandoc
- WeasyPrint

Run from the repository root:

```bash
./tools/product-reference/build.sh
```

Generated files are written to `build/product-reference/`:

```text
unit_product_reference_v_1_0_0_devlab_multi_hub_shield.md
unit_product_reference_v_1_0_0_devlab_multi_hub_shield.docx
unit_product_reference_v_1_0_0_devlab_multi_hub_shield.html
unit_product_reference_v_1_0_0_devlab_multi_hub_shield.pdf
```
