# Datasheet authoring framework

Este directorio es la fuente editable del datasheet. El contenido se mantiene
en Markdown, Pandoc ensambla los capítulos y WeasyPrint genera el PDF editorial
desde la plantilla HTML/CSS. Pandoc también produce un DOCX secundario.

`docs/` no es una fuente: es la salida publicada por el workflow.

## Estructura

```text
tools/datasheet/
├── book.yml       Metadatos y orden de los capítulos
├── reference-a4.docx Plantilla de estilos A4 para Pandoc
├── chapters/      Contenido técnico editable
└── assets/media/  Imágenes utilizadas por los capítulos
```

## Construir el documento

Requisitos:

- Pandoc
- WeasyPrint

Desde la raíz del repositorio:

```bash
./tools/datasheet/build.sh
```

Los resultados quedan en `build/datasheet/`:

```text
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.md
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.docx
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.html
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.pdf
```

## Editar o agregar un capítulo

1. Edita un archivo de `chapters/` o crea uno nuevo.
2. Si creaste un capítulo, agrégalo a `chapters:` en `book.yml`.
3. Coloca sus imágenes en `assets/media/`.
4. Usa rutas desde la raíz del repositorio:

   ```markdown
   ![Descripción](tools/datasheet/assets/media/my-image.png){width=5in}
   ```

5. Ejecuta el build y revisa el PDF.

El número visible de las secciones se conserva dentro de los títulos Markdown.
Por ejemplo:

```markdown
## 4 Connectors & Pinouts

### 4.1 General Pinout
```

## Relación con `hardware/`

`hardware/` contiene los recursos liberados del producto: esquemáticos,
pinouts, dimensiones y vistas. Los capítulos pueden enlazar esos recursos, pero
el contenido narrativo vive aquí.

Durante CI, el documento se construye en `build/`, se incorpora temporalmente a
`hardware/` y el generador normal del repositorio copia el paquete completo a
`docs/hardware/`.

## Plantillas visuales

El PDF usa:

- `templates/datasheet.html`: portada y estructura editorial.
- `styles/datasheet.css`: formato A4, encabezados, pies, colores, tablas y
  control de saltos de página.

El DOCX usa `reference-a4.docx` como documento de referencia. Puede abrirse en
Word o LibreOffice para personalizar sus estilos.

## Reglas de mantenimiento

- No edites directamente el PDF generado.
- No mantengas la misma tabla en dos capítulos.
- Conserva magnitudes y unidades en las tablas de ratings.
- Verifica que toda imagen referenciada exista.
- Revisa el PDF cuando cambien tablas, imágenes o saltos de página.
- Actualiza `version` y `date` en `book.yml` antes de una liberación.
