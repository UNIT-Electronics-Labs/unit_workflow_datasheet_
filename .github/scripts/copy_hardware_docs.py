#!/usr/bin/env python3
"""Publish hardware resources and generate a static download page."""

import html
import os
import shutil
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent.parent.parent
HARDWARE_DIR = BASE_DIR / "hardware"
DOCS_DIR = BASE_DIR / "docs"
DOCS_HARDWARE_DIR = DOCS_DIR / "hardware"
DATASHEET_BUILD_DIR = BASE_DIR / "build" / "datasheet"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}
CAD_EXTENSIONS = {
    ".step",
    ".stp",
    ".iges",
    ".igs",
    ".stl",
    ".obj",
    ".3mf",
    ".dxf",
    ".dwg",
}
DESIGN_EXTENSIONS = {
    ".kicad_pcb",
    ".kicad_sch",
    ".kicad_pro",
    ".brd",
    ".sch",
}
MANUFACTURING_EXTENSIONS = {
    ".gbr",
    ".gtl",
    ".gbl",
    ".gts",
    ".gbs",
    ".gto",
    ".gbo",
    ".drl",
    ".xln",
    ".pos",
    ".bom",
    ".ipc",
}
ARCHIVE_EXTENSIONS = {".zip", ".7z", ".tar", ".gz", ".tgz"}

CATEGORY_ORDER = {
    "Product documents": 0,
    "Pinouts": 1,
    "Board views": 2,
    "CAD and design files": 3,
    "Manufacturing files": 4,
    "Other resources": 5,
}


def format_size(size_bytes):
    """Return a compact, human-readable file size."""
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024


def classify_resource(name, extension):
    """Classify known hardware formats without requiring a file manifest."""
    lower_name = name.lower()
    category = "Other resources"
    title = Path(name).stem.replace("_", " ").replace("-", " ").title()
    description = "Hardware resource"

    if "datasheet" in lower_name:
        category = "Product documents"
        title = "Product Datasheet"
        description = (
            "Publication-ready product reference"
            if extension == ".pdf"
            else "Editable product reference"
        )
    elif "_sch_" in lower_name or "schematic" in lower_name:
        category = "Product documents"
        title = "Schematic"
        description = "Electrical schematic"
    elif "pinout" in lower_name:
        category = "Pinouts"
        language = "Spanish" if "_es." in lower_name else "English"
        title = f"Pinout — {language}"
        description = f"Connector and signal reference in {language}"
    elif "dimension" in lower_name:
        category = "Board views"
        title = "Mechanical Dimensions"
        description = "Board outline and dimensions"
    elif "topology" in lower_name:
        category = "Board views"
        title = "Board Topology"
        description = "Functional board layout"
    elif "_top_" in lower_name:
        category = "Board views"
        title = "Top View"
        description = "Top-side board view"
    elif "_btm_" in lower_name or "_bottom_" in lower_name:
        category = "Board views"
        title = "Bottom View"
        description = "Bottom-side board view"
    elif extension in CAD_EXTENSIONS:
        category = "CAD and design files"
        cad_labels = {
            ".step": ("3D CAD Model", "STEP mechanical model"),
            ".stp": ("3D CAD Model", "STEP mechanical model"),
            ".iges": ("3D CAD Model", "IGES mechanical model"),
            ".igs": ("3D CAD Model", "IGES mechanical model"),
            ".stl": ("3D Printable Model", "STL mesh model"),
            ".obj": ("3D Model", "OBJ mesh model"),
            ".3mf": ("3D Printable Model", "3MF model"),
            ".dxf": ("Mechanical Drawing", "DXF drawing"),
            ".dwg": ("Mechanical Drawing", "DWG drawing"),
        }
        title, description = cad_labels[extension]
    elif extension in DESIGN_EXTENSIONS:
        category = "CAD and design files"
        design_labels = {
            ".kicad_pcb": ("KiCad PCB Layout", "Editable PCB layout source"),
            ".kicad_sch": ("KiCad Schematic Source", "Editable schematic source"),
            ".kicad_pro": ("KiCad Project", "KiCad project configuration"),
            ".brd": ("PCB Layout Source", "Editable board layout source"),
            ".sch": ("Schematic Source", "Editable schematic source"),
        }
        title, description = design_labels[extension]
    elif extension in MANUFACTURING_EXTENSIONS:
        category = "Manufacturing files"
        if extension == ".bom" or "bom" in lower_name:
            title = "Bill of Materials"
            description = "Manufacturing bill of materials"
        elif extension == ".pos" or "pick" in lower_name or "place" in lower_name:
            title = "Pick-and-Place Data"
            description = "Component placement data"
        elif extension in {".drl", ".xln"}:
            title = "Drill File"
            description = "PCB drilling data"
        else:
            title = "Gerber File"
            description = "PCB fabrication layer"
    elif extension in ARCHIVE_EXTENSIONS:
        if any(word in lower_name for word in ("gerber", "fabrication", "manufacturing")):
            category = "Manufacturing files"
            title = "Manufacturing Package"
            description = "Compressed PCB fabrication files"
        elif any(word in lower_name for word in ("cad", "step", "model", "design")):
            category = "CAD and design files"
            title = "Design Package"
            description = "Compressed design resources"
        else:
            title = "Hardware Resource Package"
            description = "Compressed hardware resources"
    elif lower_name == "readme.md":
        title = "Hardware README"
        description = "Hardware overview and source notes"
    elif "schematics_icon" in lower_name:
        title = "Schematic Icon"
        description = "Artwork used by the hardware README"

    return category, title, description


def describe_file(file_path):
    """Build user-facing metadata from a published hardware filename."""
    name = file_path.name
    extension = file_path.suffix.lower()
    category, title, description = classify_resource(name, extension)
    relative_path = file_path.relative_to(DOCS_DIR).as_posix()
    return {
        "name": name,
        "title": title,
        "description": description,
        "category": category,
        "extension": extension,
        "type": "image" if extension in IMAGE_EXTENSIONS else "document",
        "size": file_path.stat().st_size,
        "size_human": format_size(file_path.stat().st_size),
        "path": relative_path,
        "display_path": relative_path.removeprefix("hardware/"),
        "url": quote(relative_path, safe="/"),
    }


def copy_hardware_files():
    """Copy released hardware files and generated datasheet outputs."""
    if not HARDWARE_DIR.is_dir():
        raise FileNotFoundError(f"Hardware directory not found: {HARDWARE_DIR}")

    if DOCS_HARDWARE_DIR.exists():
        shutil.rmtree(DOCS_HARDWARE_DIR)
    shutil.copytree(HARDWARE_DIR, DOCS_HARDWARE_DIR)

    if DATASHEET_BUILD_DIR.is_dir():
        for generated_file in sorted(DATASHEET_BUILD_DIR.iterdir()):
            if generated_file.suffix.lower() in {".pdf", ".docx"}:
                shutil.copy2(generated_file, DOCS_HARDWARE_DIR / generated_file.name)


def scan_published_files():
    """Return deterministic metadata for every published hardware file."""
    files = []
    for root, dirs, names in os.walk(DOCS_HARDWARE_DIR):
        dirs.sort()
        for name in sorted(names):
            if name.lower() == "schematics_icon.jpg":
                continue
            files.append(describe_file(Path(root) / name))
    return sorted(
        files,
        key=lambda item: (
            CATEGORY_ORDER[item["category"]],
            item["title"].lower(),
            item["extension"],
        ),
    )


def render_resource(item):
    """Render one accessible resource card."""
    title = html.escape(item["title"])
    description = html.escape(item["description"])
    filename = html.escape(item["display_path"])
    extension = html.escape(item["extension"].lstrip(".").upper() or "FILE")
    size = html.escape(item["size_human"])
    url = html.escape(item["url"], quote=True)

    return f"""
        <article class="resource-card" data-search="{html.escape((item['title'] + ' ' + item['path'] + ' ' + item['description']).lower(), quote=True)}">
          <div class="resource-content">
            <div class="resource-heading">
              <span class="file-type">{extension}</span>
              <span class="file-size">{size}</span>
            </div>
            <h3>{title}</h3>
            <p>{description}</p>
            <code title="{filename}">{filename}</code>
            <div class="actions">
              <button class="button primary copy-link" type="button" data-url="{url}">Copy link</button>
              <a class="button" href="{url}" target="_blank" rel="noopener">Open file</a>
            </div>
          </div>
        </article>"""


def generate_html_page(files):
    """Generate a responsive, dependency-free hardware resource page."""
    grouped = {category: [] for category in CATEGORY_ORDER}
    for item in files:
        grouped[item["category"]].append(item)

    sections = []
    for category in CATEGORY_ORDER:
        items = grouped[category]
        if not items:
            continue
        cards = "\n".join(render_resource(item) for item in items)
        sections.append(
            f"""
      <section class="resource-section">
        <div class="section-heading">
          <h2>{html.escape(category)}</h2>
          <span>{len(items)} {"file" if len(items) == 1 else "files"}</span>
        </div>
        <div class="resource-grid">{cards}
        </div>
      </section>"""
        )

    total_size = format_size(sum(item["size"] for item in files))
    images = sum(item["type"] == "image" for item in files)
    formats = len({item["extension"] for item in files})
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Multi-Hub Shield hardware documentation and downloads">
  <title>Multi-Hub Shield | Hardware Resources</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #667085;
      --line: #dfe3e8;
      --surface: #f6f7f9;
      --brand: #e53b2c;
      --brand-dark: #bd2b20;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: #fff;
      font: 16px/1.5 Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
    }}
    a {{ color: inherit; }}
    .site-header {{
      border-bottom: 1px solid var(--line);
      background: linear-gradient(135deg, #fff 35%, #f3f4f6);
    }}
    .header-content, main {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }}
    .header-content {{ padding: 56px 0 42px; }}
    .eyebrow {{
      margin: 0 0 8px;
      color: var(--brand);
      font-size: .78rem;
      font-weight: 800;
      letter-spacing: .12em;
      text-transform: uppercase;
    }}
    h1 {{ margin: 0; font-size: clamp(2rem, 5vw, 3.4rem); line-height: 1.05; }}
    .subtitle {{ max-width: 680px; margin: 16px 0 0; color: var(--muted); }}
    .summary {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px 24px;
      margin-top: 28px;
      color: var(--muted);
      font-size: .9rem;
    }}
    .summary strong {{ color: var(--ink); }}
    main {{ padding: 34px 0 64px; }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 2;
      padding: 12px 0 20px;
      background: rgba(255, 255, 255, .96);
    }}
    .search {{
      width: 100%;
      padding: 13px 16px;
      border: 1px solid var(--line);
      border-radius: 10px;
      color: var(--ink);
      background: #fff;
      font: inherit;
    }}
    .search:focus {{ outline: 3px solid rgba(229, 59, 44, .16); border-color: var(--brand); }}
    .resource-section {{ margin-top: 30px; }}
    .section-heading {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--line);
    }}
    .section-heading h2 {{ margin: 0 0 9px; font-size: 1.25rem; }}
    .section-heading span {{ color: var(--muted); font-size: .85rem; }}
    .resource-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
      gap: 16px;
    }}
    .resource-card {{
      min-width: 0;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #fff;
      transition: border-color .15s ease, transform .15s ease, box-shadow .15s ease;
    }}
    .resource-card:hover {{
      transform: translateY(-2px);
      border-color: #c6cbd2;
      box-shadow: 0 10px 28px rgba(23, 32, 42, .08);
    }}
    .resource-content {{ padding: 18px; }}
    .resource-heading {{ display: flex; justify-content: space-between; gap: 12px; }}
    .file-type {{
      padding: 3px 8px;
      border-radius: 999px;
      color: var(--brand-dark);
      background: #fff0ee;
      font-size: .72rem;
      font-weight: 800;
    }}
    .file-size {{ color: var(--muted); font-size: .78rem; }}
    .resource-card h3 {{ margin: 14px 0 4px; font-size: 1.08rem; }}
    .resource-card p {{ min-height: 24px; margin: 0 0 12px; color: var(--muted); font-size: .9rem; }}
    .resource-card code {{
      display: block;
      overflow: hidden;
      color: #727985;
      font-size: .7rem;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .actions {{ display: flex; gap: 8px; margin-top: 18px; }}
    .button {{
      display: inline-flex;
      justify-content: center;
      padding: 8px 14px;
      border: 1px solid var(--line);
      border-radius: 7px;
      cursor: pointer;
      text-decoration: none;
      font-size: .88rem;
      font-weight: 700;
      font-family: inherit;
    }}
    .button:hover {{ border-color: #aeb4bd; background: var(--surface); }}
    .button.primary {{ color: #fff; border-color: var(--brand); background: var(--brand); }}
    .button.primary:hover {{ border-color: var(--brand-dark); background: var(--brand-dark); }}
    .empty-state {{ display: none; padding: 48px 0; color: var(--muted); text-align: center; }}
    footer {{ padding: 24px 16px; border-top: 1px solid var(--line); color: var(--muted); text-align: center; font-size: .82rem; }}
    [hidden] {{ display: none !important; }}
    .visually-hidden {{
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }}
    @media (max-width: 600px) {{
      .header-content {{ padding: 38px 0 30px; }}
      main {{ padding-top: 18px; }}
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="header-content">
      <p class="eyebrow">UNIT Electronics · UE0064</p>
      <h1>Multi-Hub Shield</h1>
      <p class="subtitle">Direct links to hardware documentation and product files for use in external platforms.</p>
      <div class="summary" aria-label="Resource summary">
        <span><strong>{len(files)}</strong> files</span>
        <span><strong>{images}</strong> images</span>
        <span><strong>{formats}</strong> formats</span>
        <span><strong>{html.escape(total_size)}</strong> total</span>
      </div>
    </div>
  </header>
  <main>
    <div class="toolbar">
      <label for="resource-search" class="visually-hidden">Search hardware resources</label>
      <input id="resource-search" class="search" type="search" placeholder="Search hardware resources…" autocomplete="off">
    </div>
    {"".join(sections)}
    <p id="empty-state" class="empty-state">No resources match your search.</p>
  </main>
  <footer>UNIT Electronics hardware resources</footer>
  <script>
    const search = document.getElementById('resource-search');
    const sections = [...document.querySelectorAll('.resource-section')];
    const emptyState = document.getElementById('empty-state');
    const copyText = async (text) => {{
      try {{
        await navigator.clipboard.writeText(text);
      }} catch (error) {{
        const input = document.createElement('textarea');
        input.value = text;
        input.style.position = 'fixed';
        input.style.opacity = '0';
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        input.remove();
      }}
    }};
    document.querySelectorAll('.copy-link').forEach((button) => {{
      button.addEventListener('click', async () => {{
        const absoluteUrl = new URL(button.dataset.url, window.location.href).href;
        await copyText(absoluteUrl);
        const originalLabel = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => {{ button.textContent = originalLabel; }}, 1600);
      }});
    }});
    search.addEventListener('input', () => {{
      const query = search.value.trim().toLowerCase();
      let visibleCards = 0;
      sections.forEach((section) => {{
        let sectionCards = 0;
        section.querySelectorAll('.resource-card').forEach((card) => {{
          const match = card.dataset.search.includes(query);
          card.hidden = !match;
          sectionCards += Number(match);
        }});
        section.hidden = sectionCards === 0;
        visibleCards += sectionCards;
      }});
      emptyState.style.display = visibleCards ? 'none' : 'block';
    }});
  </script>
</body>
</html>
"""

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    page = "\n".join(line.rstrip() for line in page.splitlines()).strip() + "\n"
    (DOCS_DIR / "index.html").write_text(page, encoding="utf-8")


def main():
    """Publish the hardware resources and index page."""
    copy_hardware_files()
    files = scan_published_files()
    generate_html_page(files)
    print(f"Published {len(files)} hardware files to {DOCS_HARDWARE_DIR}")
    print(f"Generated {DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
