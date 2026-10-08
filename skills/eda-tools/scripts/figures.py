"""Write every figure in a notebook to a PNG so each one can be looked at.

    python figures.py NOTEBOOK.ipynb OUT_DIR

Files are named by cell index and the section heading the cell sits under. The script prints one
line per file written and exits 1 if the notebook has no figures.
"""
import base64
import json
import re
import sys
from pathlib import Path


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "untitled"


def write_figures(notebook, out_dir):
    cells = json.loads(Path(notebook).read_text())["cells"]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    section, written = "start", []
    for i, cell in enumerate(cells):
        source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            heading = re.search(r"^##\s+(.+)$", source, re.M)
            if heading:
                section = heading.group(1)
            continue
        n = 0
        for output in cell.get("outputs", []):
            png = output.get("data", {}).get("image/png")
            if not png:
                continue
            n += 1
            path = out_dir / f"{i:03d}-{n}-{slug(section)}.png"
            path.write_bytes(base64.b64decode("".join(png) if isinstance(png, list) else png))
            written.append(path)
    return written


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    files = write_figures(sys.argv[1], sys.argv[2])
    for path in files:
        print(path)
    print(f"\n{len(files)} figures written")
    sys.exit(0 if files else 1)
