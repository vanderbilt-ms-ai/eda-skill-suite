"""Check that the series A hypotheses were written before the data was pulled, and that the analysis
notebook carries them verbatim.

    python check_order.py PROJECT_DIR --stamp     # right after writing hypotheses.md, before the request runs
    python check_order.py PROJECT_DIR             # at verification

--stamp writes hypotheses.stamp (the file's SHA-256 and the UTC time) beside hypotheses.md.
The check reads the stamp and reports:
  ERROR  hypotheses.md has changed since it was stamped
  ERROR  a file in data/raw/ is older than the stamp (the data was pulled first)
  ERROR  the analysis notebook has no markdown cell containing hypotheses.md's text
  ERROR  hypotheses.md, decisions.md, or verification.md holds non-ASCII characters
  WARN   no stamp was written; only file modification times can be compared, and those are weak
Exit code 1 on any ERROR.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp(project):
    hyp = Path(project) / "hypotheses.md"
    if not hyp.exists():
        raise SystemExit("ERROR  no hypotheses.md to stamp")
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    (Path(project) / "hypotheses.stamp").write_text(f"{sha(hyp)} {now}\n")
    print(f"stamped hypotheses.md at {now}")


def check(project):
    project = Path(project)
    hyp, stamp_file, raw = project / "hypotheses.md", project / "hypotheses.stamp", project / "data" / "raw"
    findings = []
    if not hyp.exists():
        return [("ERROR", "no hypotheses.md in the project folder")]
    raw_files = [p for p in raw.rglob("*") if p.is_file()] if raw.exists() else []
    if stamp_file.exists():
        digest, when = stamp_file.read_text().split()
        stamped = datetime.fromisoformat(when)
        if digest != sha(hyp):
            findings.append(("ERROR", "hypotheses.md has changed since it was stamped"))
        for p in raw_files:
            modified = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
            if modified < stamped:
                findings.append(("ERROR", f"{p.relative_to(project)} predates the hypotheses stamp"))
    else:
        findings.append(("WARN", "no hypotheses.stamp; comparing modification times only"))
        for p in raw_files:
            if p.stat().st_mtime < hyp.stat().st_mtime:
                findings.append(("ERROR", f"{p.relative_to(project)} is older than hypotheses.md"))
    for name in ("hypotheses.md", "decisions.md", "verification.md"):
        f = project / name
        if f.exists():
            bad = sum(1 for line in f.read_text().splitlines() if any(ord(ch) > 127 for ch in line))
            if bad:
                findings.append(("ERROR", f"{name}: {bad} lines with non-ASCII characters (em dashes, curly quotes)"))
    notebooks = sorted(project.glob("*analysis*.ipynb"))
    if not notebooks:
        findings.append(("ERROR", "no *analysis*.ipynb in the project folder"))
    else:
        wanted = normalize(hyp.read_text())
        cells = json.loads(notebooks[0].read_text())["cells"]
        texts = [normalize(c["source"] if isinstance(c["source"], str) else "".join(c["source"]))
                 for c in cells if c["cell_type"] == "markdown"]
        if not any(wanted in t for t in texts):
            findings.append(("ERROR", f"{notebooks[0].name} has no markdown cell containing hypotheses.md verbatim"))
    return findings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if "--stamp" in sys.argv:
        stamp(sys.argv[1])
        sys.exit(0)
    results = check(sys.argv[1])
    for level, message in results:
        print(f"{level:5}  {message}")
    errors = sum(1 for level, _ in results if level == "ERROR")
    print(f"\n{errors} errors, {len(results) - errors} warnings")
    sys.exit(1 if errors else 0)
