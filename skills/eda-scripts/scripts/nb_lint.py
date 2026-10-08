"""Check an analysis notebook against the suite's notebook, figure, and writing standards.

    python nb_lint.py NOTEBOOK.ipynb            # lint
    python nb_lint.py NOTEBOOK.ipynb --trace    # also trace quoted numbers to cell outputs

ERROR lines are breaches of a rule; WARN lines need a human look. Exit code 1 if any ERROR.
Numbers drawn inside a figure (a title, a legend) cannot be traced from the notebook file; --trace
lists them as warnings, and they are checked by looking at the figure.

What it can check automatically (everything else in the standards needs reading):
  notebook  - prose print statements (top level or inside a loop); analysis sections without a
              "What we found" cell; errors or unexecuted cells; absolute paths
  figures   - plotting cells with no title or no axis labels (directly, or through a notebook-defined
              helper that sets them or takes them as parameters); bar charts whose y-limits are set
              to start above zero
  writing   - non-ASCII punctuation; stock phrases and idioms (ERROR); variable names in findings
              (ERROR); reversals, framing sentences, wording that may claim more than the record,
              and markdown cells over 200 words (WARN)
  hypotheses - a "Hypothesis ...", "Digging deeper ...", or "Lens ..." section whose opening
              markdown has no "Refuted if" (ERROR); a notebook with "## First hypotheses" and no
              "## Second hypotheses" section (ERROR)
  --trace   - numbers quoted in the markdown that no output shows:
              "What we found" cells     against the outputs above them (also inside a synthesis)
              other cells under a Synthesis, Memo, or Recap heading
                                        against every output in the notebook (they summarize)
              the brief                 the numbers under its "The observation" / "What was
                                        observed" label (not the quoted request), against every
                                        output here and in a sibling *step0* or *setup* notebook
              A number followed by 's (a name such as 538's) is not traced.
              A number matches an output if they are equal after dropping commas, $ and %, ignoring
              sign ("$1,234 less" matches -1234.0), with the output rounded to the number's decimals;
              a percent ("16.3 percent", "93 to 100 percent") also matches a share (0.163).
              Section references ("section 5.3", heading numbers like "5.15") are not traced.
"""
import bisect
import json
import re
import sys
from pathlib import Path

PLOT_CALLS = re.compile(r"\.(bar|barh|plot|scatter|hist|boxplot|imshow|pcolormesh|contourf?)\(|"
                        r"sns\.\w+\(|plt\.(bar|plot|scatter|hist)\(")
STOCK_PHRASES = ["it is worth noting", "it's worth noting", "let's dive", "dive into", "interestingly",
                 "in conclusion", "at the end of the day", "tells a story", "tell a story",
                 "the data speaks", "numbers don't lie", "perfect storm", "game changer",
                 "needle in a haystack", "tip of the iceberg", "paints a picture", "a tale of",
                 "cry wolf", "cries wolf", "smoking gun", "silver bullet", "low-hanging fruit",
                 "move the needle", "moves the needle", "double-edged", "elephant in the room",
                 "in a nutshell", "the bottom line is", "it goes without saying"]
# A sentence that announces what the text is about to do instead of doing it.
FRAMING = re.compile(r"(?im)^(?:[ \t]*(?:[-*+]|\d+[.)])?[ \t]*(?:\*\*[^*\n]+\*\*[ \t]*)?)"
                     r"(?:This (?:section|notebook|part|cell|step)\b|In this (?:section|notebook|part)\b|"
                     r"We (?:will|now) |Below,? we |The next section\b|What follows\b|Here we )")
# The reversal: "not X - but Y", "it's not X, it's Y".
REVERSAL = re.compile(r"(?i)\bnot\b[^.!?\n]{2,60}?\s-\s(?:but|until|yet|it'?s)\b|\bit'?s not\b[^.!?\n]{2,60}?,\s*it'?s\b")
# Words that may claim more than the record holds; a person decides each one.
BEYOND_RECORD = re.compile(r"(?i)\bfell as\b|\bset a record\b|\ba record\b(?! of)|\brecord-breaking\b|"
                           r"\bdid not happen\b|\bcaused?\b|\bbecause of\b|\bled to\b|\bdue to\b")
WALL_OF_TEXT = 200   # words in one markdown cell, tables excluded
BAR_CALL = re.compile(r"\.bar\(|\.barh\(|kind\s*=\s*[\"']barh?[\"']|\.plot\.barh?\(")
NON_ASCII_PUNCT = {"\u2014": "em dash", "\u2013": "en dash", "\u2192": "arrow", "\u2190": "arrow",
                   "\u201c": "curly quote", "\u201d": "curly quote", "\u2018": "curly quote",
                   "\u2019": "curly quote", "\u2026": "ellipsis character"}
NO_FINDING_SECTIONS = ("setup", "hypotheses", "limits", "memo", "recap", "naming", "where the data",
                       "save", "provenance", "the request")
NEEDS_FINDING = ("audit", "quality", "missing", "hypothes", "digging", "synthesis", "observation",
                 "check", "lens", "cluster", "regress", "classif")
SUMMARY_SECTIONS = ("synthesis", "memo", "recap")
FINDING = re.compile(r"^\s*\*\*what we found", re.I)
# The whole bold label, so the closing ** is not left behind to pair with the next bold span.
FINDING_LABEL = re.compile(r"^\s*\*\*what we found[^*]*\*\*[.:]?", re.I)
HEADING_NUMBER = re.compile(r"^#{1,6}[ \t]+(\d+(?:\.\d+)*)\.?(?=\s)", re.M)

# What sets each figure element, inside a helper's body: a call with an argument other than an empty
# string or None, or the keyword argument (ax.set(title=...), df.plot(title=...)).
SETTERS = {"title": ("set_title", "suptitle", "plt.title"),
           "xlabel": ("set_xlabel", "supxlabel", "plt.xlabel"),
           "ylabel": ("set_ylabel", "supylabel", "plt.ylabel")}
EMPTY = r"(?!\s*(?:\)|\"\"|''|None\b))"


def src(cell):
    return cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])


def output_text(cell):
    parts = []
    for out in cell.get("outputs", []):
        if "text" in out:
            parts.append(out["text"] if isinstance(out["text"], str) else "".join(out["text"]))
        data = out.get("data", {})
        for key in ("text/plain", "text/html"):
            if key in data:
                value = data[key] if isinstance(data[key], str) else "".join(data[key])
                parts.append(re.sub(r"<[^>]+>", " ", value))
    return "\n".join(parts)


def code_numbers(text):
    """Numbers written in code (thresholds, constants) count as shown."""
    return " ".join(re.findall(r"(?<![\w.])\d[\d,]*\.?\d*", text))


def helper_credits(cells):
    """Notebook-defined helpers -> (draws, the figure elements it sets). A helper sets an element if
    its body sets it (set_title, ax.set(xlabel=...), suptitle, ...) or it has a parameter with that
    name. Only helpers that draw make a cell a plotting cell; any helper can supply a title or label."""
    helpers = {}
    for cell in cells:
        if cell["cell_type"] != "code":
            continue
        text = src(cell)
        for match in re.finditer(r"^def (\w+)\(((?:[^()]|\([^()]*\))*)\)\s*(?:->[^:\n]*)?:[ \t]*\n"
                                 r"((?:[ \t]+.*\n?|\n)*)", text, re.M):
            name, args, body = match.groups()
            params = {re.split(r"[=:]", a)[0].strip().lstrip("*") for a in args.split(",")}
            sets = set()
            for element, calls in SETTERS.items():
                call = "|".join(re.escape(c) for c in calls)
                if (element in params or re.search(rf"(?:{call})\({EMPTY}", body)
                        or re.search(rf"[(,]\s*{element}\s*={EMPTY}", body)):
                    sets.add(element)
            draws = bool(PLOT_CALLS.search(body) or "subplots(" in body)
            if draws or sets:
                helpers[name] = (draws, sets)
    return helpers


class NumberPool:
    """Absolute values of every number in a set of texts, for tolerance lookups."""

    TOKEN = re.compile(r"(?<![\w.])-?\d[\d,]*\.?\d*(?:[eE][+-]?\d+)?")

    def __init__(self, texts=()):
        self.values, self.sorted = set(), None
        for text in texts:
            self.add(text)

    def add(self, text):
        for token in self.TOKEN.findall(text):
            try:
                self.values.add(abs(float(token.replace(",", ""))))
            except ValueError:
                pass
        self.sorted = None

    def near(self, target, tol):
        if self.sorted is None:
            self.sorted = sorted(self.values)
        k = bisect.bisect_left(self.sorted, target - tol)
        return k < len(self.sorted) and self.sorted[k] <= target + tol


def setup_notebook_texts(path):
    """Outputs and code numbers of a sibling setup notebook, whose numbers a brief may quote."""
    here = Path(path).resolve()
    texts, headings = [], set()
    siblings = {p.resolve() for pattern in ("*step0*.ipynb", "*setup*.ipynb") for p in here.parent.glob(pattern)}
    for sibling in sorted(siblings - {here}):
        for cell in json.loads(sibling.read_text())["cells"]:
            if cell["cell_type"] == "code":
                texts += [output_text(cell), code_numbers(src(cell))]
            else:
                headings.update(HEADING_NUMBER.findall(src(cell)))
    return texts, headings


def brief_observation(text):
    """The lines of the brief under a heading or bold label naming the observation ("The
    observation", "What was observed"), up to the next label; quoted request lines are skipped."""
    kept, inside, paragraph_start = [], False, True
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            paragraph_start = True
            continue
        # A heading, or bold text opening a paragraph (not a wrapped line or a bullet that starts bold).
        label = re.match(r"#+\s+(.*)", stripped) or (paragraph_start and re.match(r"\*\*([^*]+)\*\*", stripped))
        if label:
            inside = "observ" in next(g for g in label.groups() if g is not None).lower()
            if inside:
                line = stripped[label.end():]
        if inside:
            kept.append(line)
        paragraph_start = not stripped
    return "\n".join(kept)


def lint(path, trace=False):
    nb = json.loads(Path(path).read_text())
    cells = nb["cells"]
    helpers = helper_credits(cells)
    findings = []

    def report(level, i, rule, detail=""):
        findings.append((level, i, rule, detail))

    headings = {n for cell in cells if cell["cell_type"] == "markdown" for n in HEADING_NUMBER.findall(src(cell))}
    every_output = NumberPool(t for cell in cells if cell["cell_type"] == "code"
                              for t in (output_text(cell), code_numbers(src(cell))))
    brief = next((i for i, cell in enumerate(cells) if cell["cell_type"] == "markdown"), None)

    section, section_has_code, section_has_finding, section_start = None, False, False, None
    section_has_image = False
    pending_refutation = None   # [level, heading cell] until "Refuted if" appears before the first code cell

    def section_kind(name):
        lowered = (name or "").lower()
        if lowered.startswith("hypothesis"):
            return "ERROR"
        if lowered.startswith("digging deeper") or lowered.startswith("lens"):
            return "ERROR"
        return None

    def close_section():
        if section and section_has_code and not section_has_finding:
            name = section.lower()
            needs = section_has_image or any(word in name for word in NEEDS_FINDING)
            if needs and not any(word in name for word in NO_FINDING_SECTIONS):
                report("ERROR", section_start, "notebook: section has code but no 'What we found' cell",
                       section)

    seen_outputs = NumberPool()
    for i, cell in enumerate(cells):
        text = src(cell)
        if cell["cell_type"] == "markdown":
            heading = re.search(r"^##\s+(.+)$", text, re.M)
            if heading:
                close_section()
                section, section_has_code, section_has_finding, section_start = heading.group(1), False, False, i
                section_has_image = False
            summary = next((word for word in SUMMARY_SECTIONS if section and word in section.lower()), None)
            is_finding = bool(FINDING.search(text))
            if is_finding:
                section_has_finding = True
                check_finding(text, i, report)
                if trace:
                    trace_numbers(FINDING_LABEL.sub("", text), i, report, seen_outputs, headings,
                                  "in a finding not found in any output above")
            elif trace and summary:
                trace_numbers(text, i, report, every_output, headings,
                              f"in the {summary} not found in any output")
            if trace and i == brief:
                setup_texts, setup_headings = setup_notebook_texts(path)
                where = "this notebook's or the setup notebook's" if setup_texts else "this notebook's"
                pool = NumberPool(setup_texts)
                pool.values |= every_output.values
                trace_numbers(brief_observation(text), i, report, pool, headings | setup_headings,
                              f"in the brief's observation not found in {where} outputs")
            for ch, name in NON_ASCII_PUNCT.items():
                if ch in text:
                    report("ERROR", i, f"writing: non-ASCII punctuation ({name})")
            lowered = text.lower()
            for phrase in STOCK_PHRASES:
                if phrase in lowered:
                    report("ERROR", i, f"writing: stock phrase or idiom '{phrase}'")
            for match in FRAMING.finditer(text):
                report("WARN", i, "writing: framing sentence (say the content, not what comes next)",
                       text[match.start():match.start() + 70].strip().replace("\n", " "))
            for match in REVERSAL.finditer(text):
                report("WARN", i, "writing: reversal construction", match.group()[:70])
            for match in BEYOND_RECORD.finditer(text):
                report("WARN", i, "writing: wording may claim more than the record shows", match.group())
            words = sum(len(line.split()) for line in text.splitlines() if not line.lstrip().startswith("|"))
            is_hypotheses_cell = bool(re.search(r"^##\s+(?:First |Second )?hypotheses", text, re.I | re.M))
            if words > WALL_OF_TEXT and not is_hypotheses_cell:   # the hypotheses cell is inserted verbatim
                report("WARN", i, f"writing: markdown cell of {words} words (over {WALL_OF_TEXT}); split or cut")
            if heading and section_kind(section):
                pending_refutation = [section_kind(section), i]
            if pending_refutation and "refut" in lowered:
                pending_refutation = None
            continue

        # code cell
        if pending_refutation:
            level, at = pending_refutation
            report(level, at, "hypotheses: section states no 'Refuted if' before its first code cell", section)
            pending_refutation = None
        section_has_code = True
        if any("image/png" in out.get("data", {}) for out in cell.get("outputs", [])):
            section_has_image = True
        if cell.get("execution_count") is None and text.strip():
            report("ERROR", i, "notebook: cell not executed (restart and run all)")
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                report("ERROR", i, "notebook: cell raised an error", out.get("ename", ""))
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("print(") and re.search(r"print\(\s*f?[\"']", stripped):
                report("ERROR", i, "notebook: prose print statement (show a chart or labelled table)",
                       stripped[:70])
                break
        if re.search(r"[\"'](/Users/|/home/|C:\\\\)", text) or "os.chdir" in text:
            report("ERROR", i, "notebook: absolute path or chdir")
        is_def_only = text.lstrip().startswith("def ") and not re.search(r"^\S", text.split("\n", 1)[-1], re.M)
        if not is_def_only:
            check_figure(text, i, report, helpers)
        seen_outputs.add(output_text(cell))
        seen_outputs.add(code_numbers(text))  # thresholds set in code
    close_section()
    all_headings = " ".join(src(c) for c in cells if c["cell_type"] == "markdown")
    if re.search(r"^##\s+First hypotheses", all_headings, re.I | re.M) and \
            not re.search(r"^##\s+Second hypotheses", all_headings, re.I | re.M):
        report("ERROR", 0, "hypotheses: no '## Second hypotheses (from the data)' section after the data-quality checks")
    return findings


def check_figure(text, i, report, helpers):
    called = [h for h in helpers if re.search(rf"\b{h}\(", text) and not re.search(rf"def {h}\(", text)]
    plots = bool(PLOT_CALLS.search(text)) or any(helpers[h][0] for h in called)
    if not plots:
        return
    via_helper = lambda element: any(element in helpers[h][1] for h in called)
    if not (re.search(r"title\s*=|set_title\(|suptitle\(|plt\.title\(", text) or via_helper("title")):
        report("ERROR", i, "figure: no title")
    if not (re.search(r"xlabel|set_xlabel", text) or via_helper("xlabel")):
        report("ERROR", i, "figure: no x-axis label")
    if not (re.search(r"ylabel|set_ylabel", text) or via_helper("ylabel")):
        report("ERROR", i, "figure: no y-axis label")
    lim = re.search(r"ylim\s*=?\s*\(?\s*\(?\s*([0-9.]+)", text)
    if lim and BAR_CALL.search(text) and float(lim.group(1)) > 0:
        report("ERROR", i, "figure: bar chart y-axis does not start at zero")


def check_finding(text, i, report):
    body = FINDING_LABEL.sub("", text)
    for token in re.findall(r"`([a-z]+_[a-z0-9_]+)`|\b([a-z]+_[a-z0-9_]+)\b", body):
        name = token[0] or token[1]
        report("ERROR", i, "writing: variable name in a finding", name)
        break


NUMBER = re.compile(r"(?<![\w.])-?\d[\d,]*\.?\d*%?")
# "16.3 percent", and every number of a range or pair that ends in one: "93 to 100 percent",
# "63 against 33 percent", "2.5 and 1.1 percent".
PERCENT_AFTER = re.compile(r"(?:\s*(?:to|and|or|against|versus|vs\.?|,|-)\s*-?\d[\d,]*\.?\d*%?)*"
                           r"\s*(?:%|percent|per cent|percentage)", re.I)
SECTION_REF = re.compile(r"\bsections?\s+(?:\d[\d.]*\s*(?:,\s*(?:and\s+|or\s+)?|and\s+|or\s+|to\s+|-\s*))*$", re.I)


def trace_numbers(body, i, report, pool, headings, where):
    body = re.sub(r"^#+\s.*$", "", body, flags=re.M)  # a heading's own numbers are labels
    for match in NUMBER.finditer(body):
        token = match.group()
        raw = token.rstrip("%").replace(",", "").lstrip("-").rstrip(".")
        try:
            value = float(raw)
        except ValueError:
            continue
        if SECTION_REF.search(body[max(0, match.start() - 60):match.start()]):
            continue  # "section 5.3", "sections 5.3 and 5.11"
        if body[match.end():match.end() + 2] in ("'s", "\u2019s"):
            continue  # a name, such as 538's
        if not token.startswith("-") and not token.endswith("%") and raw in headings:
            continue  # a heading number, "5.15"
        decimals = len(raw.split(".")[1]) if "." in raw else 0
        if decimals == 0 and (value <= 12 or 1900 <= value <= 2100):
            continue  # small counts, ordinals, and years are usually prose
        tol = 0.5 * 10 ** -decimals + 1e-9
        percent = token.endswith("%") or PERCENT_AFTER.match(body, match.end())
        if pool.near(value, tol) or (percent and pool.near(value / 100, tol / 100)):  # 16.3% vs 0.163
            continue
        report("WARN", i, f"trace: number {where}", token)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    results = lint(sys.argv[1], trace="--trace" in sys.argv)
    for level, i, rule, detail in results:
        print(f"{level:5} cell {i:>3}  {rule}" + (f"  [{detail}]" if detail else ""))
    errors = sum(1 for r in results if r[0] == "ERROR")
    print(f"\n{errors} errors, {len(results) - errors} warnings")
    sys.exit(1 if errors else 0)
