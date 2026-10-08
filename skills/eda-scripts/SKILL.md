---
name: eda-scripts
description: Runs the scripts the eda- skills call: the notebook lint and number trace, the download helper, the figure extractor, and the hypotheses-before-data check. Use whenever another eda- skill names a script.
---

# The scripts

**Inputs.** A notebook, a project folder, or a list of pieces to download, depending on the
script.

**Produces.** Lint output, a table of downloads, PNG files, or a pass/fail report, as listed
below. Every script the suite uses lives in this folder, once, so that no notebook rewrites one.
All need Python 3 and `pandas`; executing a notebook needs `nbformat` and `jupyter`.

The folder is `~/.claude/skills/eda-scripts/scripts/` or `.claude/skills/eda-scripts/scripts/`,
whichever the install used. Run the scripts from there. Only `fetch.py` is copied into the
project, because the setup notebook imports it.

## nb_lint.py: the notebook lint and number trace

```bash
python scripts/nb_lint.py NOTEBOOK.ipynb --trace
```

ERROR lines are breaches; WARN lines need a person's decision. The exit code is 1 on any ERROR.

Errors: a print statement that narrates a result, at the top level or inside a loop; a section
that tests something with no "What we found" cell; a hypothesis, digging-deeper, or model section
with no "Refuted if" before its first code cell; a notebook with first hypotheses and no "Second
hypotheses" section; a cell not executed; a cell that raised; an
absolute path; a plotting cell with no title or axis label (a helper that sets them counts); a
bar chart whose y-axis starts above zero; non-ASCII punctuation; a stock phrase or idiom; a
column name in a finding.

Warnings: a framing sentence; a reversal; wording that may claim more than the record ("fell as",
"a record", "caused"); a markdown cell over 200 words; and, with `--trace`, every number in a
finding, the synthesis, the memo, the recap, or the brief's observation that no output shows. A
number drawn inside a figure cannot be traced from the file; check it on the figure.

## fetch.py: download each piece once and check it

Copy the file into the project as `tools/fetch.py`, with an empty `tools/__init__.py` beside it,
and import it in the setup notebook:

```python
from tools.fetch import fetch_all, csv_check
pieces = [{"name": "2024-01", "url": URL, "params": {...}, "dest": "data/raw/2024-01.csv",
           "check": csv_check(date_col="DATE", start="2024-01-01", end="2024-01-31", min_rows=28)}]
fetch_all(pieces, date_col="DATE")
```

`fetch_all` returns the table the coverage check shows: piece, status, rows, first, last, reason.
A piece already on disk that passes its check is not requested again. A response that fails its
check is not saved, and the piece is listed as failed with the reason. The same call, run again,
requests only the failed pieces. `csv_check` is the check for a CSV piece; write a different
check for another format.

## figures.py: write every figure to PNG

```bash
python scripts/figures.py NOTEBOOK.ipynb figures/
```

One PNG per figure, named by cell index and section. Open each one.

## check_order.py: the first hypotheses came before the data

```bash
python scripts/check_order.py PROJECT_DIR --stamp    # right after hypotheses.md is written
python scripts/check_order.py PROJECT_DIR            # at verification
```

`--stamp` records the file's hash and the time in `hypotheses.stamp`. The check reports a changed
file, a file in `data/raw/` older than the stamp, an analysis notebook that does not hold
`hypotheses.md` verbatim, and non-ASCII characters in `hypotheses.md`, `decisions.md`, or
`verification.md`. Without a stamp it compares file modification times, which a copy or a
checkout can reset, and says so.
