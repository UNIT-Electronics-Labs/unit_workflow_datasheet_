# Datasheet authoring framework

Este directorio es la fuente editable del datasheet. El contenido se mantiene
en Markdown, Pandoc ensambla los capítulos en un DOCX y LibreOffice genera el
PDF final.

`docs/` no es una fuente: es la salida publicada por el workflow.

## Estructura

```text
datasheet/
├── book.yml       Metadatos y orden de los capítulos
├── reference-a4.docx Plantilla de estilos A4 para Pandoc
├── chapters/      Contenido técnico editable
└── assets/media/  Imágenes utilizadas por los capítulos
```

Los capítulos actuales fueron migrados desde
`template/unit_datasheet_v_1_0_0_devlab_multi_hub_shield.docx`.

## Construir el documento

Requisitos:

- Pandoc
- LibreOffice Writer

Desde la raíz del repositorio:

```bash
./scripts/build_datasheet.sh
```

Los resultados quedan en `build/datasheet/`:

```text
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.md
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.docx
unit_datasheet_v_1_0_0_devlab_multi_hub_shield.pdf
```

## Editar o agregar un capítulo

1. Edita un archivo de `chapters/` o crea uno nuevo.
2. Si creaste un capítulo, agrégalo a `chapters:` en `book.yml`.
3. Coloca sus imágenes en `assets/media/`.
4. Usa rutas desde la raíz del repositorio:

   ```markdown
   ![Descripción](datasheet/assets/media/my-image.png){width=5in}
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

## Plantilla visual

Pandoc usa `reference-a4.docx` como documento de referencia. Esta plantilla
controla estilos, tamaño de página, encabezados y pies. Puede abrirse en Word o
LibreOffice para personalizar los estilos.

El DOCX completo de `template/` se conserva como fuente histórica de la
migración. No se usa directamente como referencia porque contiene relaciones
internas de Google Docs que generan un DOCX incompatible al reutilizarlo con
Pandoc.

## Reglas de mantenimiento

- No edites directamente el PDF generado.
- No mantengas la misma tabla en dos capítulos.
- Conserva magnitudes y unidades en las tablas de ratings.
- Verifica que toda imagen referenciada exista.
- Revisa el PDF cuando cambien tablas, imágenes o saltos de página.
- Actualiza `version` y `date` en `book.yml` antes de una liberación.
