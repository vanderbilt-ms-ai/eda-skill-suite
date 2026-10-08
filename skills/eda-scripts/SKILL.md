---
name: eda-scripts
description: The scripts the EDA skills call: the notebook lint and number trace, the cached and checked download helper, the figure extractor, and the hypotheses-before-data check. Use whenever another EDA skill names a script, or when a notebook needs to fetch data, be linted, or have its figures viewed.
---

# EDA tools

Every script the suite uses lives here, once. The other skills name the script; this file says
what it does and how to run it. All scripts need Python 3 and `pandas`; the lint also needs
`nbformat` installed so notebooks execute.

Find this folder with `ls ~/.claude/skills/eda-scripts/scripts` or `ls .claude/skills/eda-scripts/scripts`
(whichever the install used), and run the scripts from there. Only `fetch.py` is copied into the
project, because the notebook imports it.

## nb_lint.py: the notebook lint and number trace

```bash
python scripts/nb_lint.py NOTEBOOK.ipynb --trace
```

ERROR lines are breaches; WARN lines need a person's decision. Exit code 1 on any ERROR. It checks:
- notebook: prose print statements; a section that tests something but has no "What we found"
  cell; a hypothesis, digging-deeper, or lens section with no "Refuted if"; unexecuted cells; cells that raised; absolute
  paths.
- figures: a plotting cell with no title or axis labels (helpers that set them count); a bar
  chart whose y-axis starts above zero.
- writing: non-ASCII punctuation; stock phrases and idioms; a variable name in a finding; a
  reversal; a framing sentence; a markdown cell over 200 words; wording that may claim more than
  the record ("fell as", "a record", "caused").
- `--trace`: every number in a finding, the synthesis, the memo, the recap, and the brief's
  observation that no output shows. A number drawn inside a figure cannot be traced from the file
  and is listed as a warning; check it on the figure.

## fetch.py: fetch each piece once, check it, keep the raw file

Copy it into the project as `tools/fetch.py` (create an empty `tools/__init__.py` beside it) and
import it in the setup notebook. `fetch_all(pieces, date_col=...)` returns the table the
data-quality coverage check shows: piece, status, rows, first, last, reason. A piece already on
disk that passes its check is not requested; a response that fails its check is not saved; the
same call re-requests only the failed pieces. `csv_check(date_col, start, end, min_rows)` is the
check for a CSV piece; write a different check for another format.

## figures.py: write every figure to PNG

```bash
python scripts/figures.py NOTEBOOK.ipynb figures/
```

One PNG per figure, named by cell index and section. Open each one.

## check_order.py: hypotheses before data

```bash
python scripts/check_order.py PROJECT_DIR --stamp    # right after writing hypotheses.md
python scripts/check_order.py PROJECT_DIR            # at verification
```

The stamp records the file's hash and the time. The check reports a changed file, a raw data
file older than the stamp, and an analysis notebook that does not carry `hypotheses.md` verbatim.
