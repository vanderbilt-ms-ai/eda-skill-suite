---
name: eda-write-notebook
description: Keeps analysis notebooks clear, reproducible, and easy to follow. Owns the section structure, the cells-show rule, naming, size, and code rules. Use whenever creating, editing, or reviewing a Jupyter notebook for data analysis.
---

# Notebook standards

An analysis notebook is an argument a reader can follow: someone who is not a data scientist reads
the markdown and understands what was asked, what was done, and what was found; a colleague re-runs
the code and gets the same numbers. Every rule below serves one of those two readers. The lint in
`eda-scripts` checks what it can; run it after writing or editing a notebook.

## Structure

1. Title and brief. The first cell is the brief (`eda-write-hypotheses`, The brief).
2. Setup cell. Imports and the data load, nothing else. Data comes from the files the setup
   notebook wrote (`data/...`), by relative path.
3. One section per step of the investigation, in the order it happened, with a `## ` heading that
   names the subject ("Hypothesis 1 - Poll error by sample size, 2020", "Digging deeper - State
   error against the state's result, 2012"). A reader skimming only the headings sees the
   investigation's path.
4. Each section has three parts, in this order:
   - Opening markdown that says what the measure is, how the code derives it, why it bears on the
     hypothesis, and what result would refute it. A section that tests a hypothesis opens with the
     hypothesis.
   - Code cells whose output shows the result.
   - A "**What we found.**" markdown cell, written after the code has run and from its output,
     that states the finding with the number that decides it and, for a hypothesis, the verdict in
     bold (`eda-test-hypothesis`, The verdict).
   Lens sections add two more parts (`eda-model`, Output of every lens section).
5. Closing sections: synthesis, limits (what the analysis cannot tell the stakeholder), the memo,
   and the recap table.

## Cells show, markdown interprets

- A code cell's output is a chart (a multi-panel chart when comparing two things) and, where exact
  numbers matter, a labelled table (a DataFrame or Series with readable column names; use
  `.rename(columns={...})` at display time). A regression's slope and r go on its chart.
- Never narrate results in print statements (`print("share that overstated:", x)`) and then
  interpret them below. A wall of labelled numbers does not show which one matters. Pass/fail
  checklists are `pd.Series(checks)`.
- Every number the markdown quotes is visible in a cell output above it (a table, a chart title or
  legend, a labelled value). This includes the brief (whose numbers come from the setup notebook's
  last section, under a "**What was observed.**" label), the synthesis, the memo, and the recap;
  `nb_lint.py --trace` checks all of them. The trace only shows that a number appears somewhere;
  read each one against the table it comes from.
- One idea per cell. If a cell needs a paragraph of explanation in the middle, split it.

## Naming

- Rename source columns once, right after loading, through one explicit mapping
  (`POLL_NAMES = {"samplesize": "sample_size", "margin_poll": "poll_margin_pts", ...}`), and
  explain the convention in markdown before it.
- lower_snake_case; the unit in the name (`poll_margin_pts`, `earnings_usd`); the same quantity
  has the same name in every file; codes become words (`FM-15` to `routine`).
- Source names appear only where an API or file format requires them.
- Variables are named in code and nowhere else (`eda-write-prose`, No variable names).

## Size

A reader works through a notebook in one sitting:
- a setup notebook of about 50 to 80 cells and 200 to 350 lines of code, with the data-quality
  section inside the budget `eda-check-data` sets;
- an analysis notebook of about 60 to 80 cells and 200 to 300 lines of code, with 10 to 15
  figures;
- markdown lengths as `eda-write-prose` (Length) sets them.
Going well past this scale usually means sections that do not serve the questions, or code doing
more than the lesson needs.

## Code

- Simple enough for a student to read line by line: one-line groupbys; `assign` for new columns; a
  boolean mask with a name (`final_week = ...`) instead of nested `np.where`; a plain DataFrame
  built from named Series; a code cell of about 15 lines or fewer. No clever plumbing the lesson
  does not need.
- A small helper function only for a chart or a calculation repeated many times; it takes its data
  as arguments. The download helper comes from `eda-scripts`, not from the notebook.
- Colors set where the plot is drawn; no module-level style constants.
- Comments explain why, never restate what the line does. Most cells need no comment because the
  markdown above explains them.
- Randomness gets a fixed seed (`random_state=0`).
- Raw downloads stay unchanged on disk; cleaning happens in code, so it can be re-run.

## Runs top to bottom

- Restart the kernel and run all before handing over: no errors, no stale outputs, no cell that
  depends on an out-of-order run. `jupyter nbconvert --to notebook --execute --inplace NB.ipynb`.
- Relative paths only; no `os.chdir`, no absolute paths, no machine-specific folders.

## Student versions

This suite produces the analyst's notebooks. A student version (blanks, placeholder findings, a
prediction prompt, a helpers-only notebook) is a teaching artifact with its own rules, owned by the
course's case-study skill, not by this suite.

## Reference

- `references/examples.md`: weak and strong versions of the same cells, from case-study drafts.
