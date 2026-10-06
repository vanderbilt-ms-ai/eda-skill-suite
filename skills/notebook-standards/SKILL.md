---
name: notebook-standards
description: The rules every exploratory data analysis (EDA) Jupyter notebook follows - section structure, the explanation that comes before each test, cells that show results as charts and labelled tables instead of prose print statements, column naming, simple code, comments, and a notebook that runs top to bottom. Use this skill whenever you create, edit, or review a Jupyter notebook for data analysis, or when another EDA skill writes cells into one, even if the request only says "add a cell" or "clean up this notebook".
---

# Notebook standards

An analysis notebook is an argument a reader can follow: someone who is not a data scientist
reads the markdown and understands what was asked, what was done, and what was found; a colleague
re-runs the code and gets the same numbers. Every rule below serves one of those two readers.

Run `scripts/nb_lint.py <notebook.ipynb>` after writing or editing a notebook, and fix everything it
reports before handing the notebook over. Its warnings need a human look; its errors are breaches.

## Structure

1. **Title and brief.** The first cell names the case and states the situation: who the analyst is,
   who is asking, what was observed (with its numbers), and the question or questions. See
   `writing-standards` for the observation-before-question rule.
2. **Setup cell.** Imports and the data load, nothing else. Data comes from the files the setup
   notebook wrote (`data/...`), by relative path.
3. **One section per step of the investigation**, in the order the investigation happened, with a
   `## ` heading that names the subject ("Hypothesis 1 - Poll error by sample size, 2020",
   "Digging deeper - State error against the state's result, 2012"). A reader skimming only the headings should
   see the investigation's path.
4. **Each section has three parts, in this order:**
   - **Opening markdown** that says what the measure is, how the code derives it, why it bears on
     the hypothesis or question, and what result would support or refute it. Define every
     statistic at first use (slope, intercept, r, R-squared, silhouette, accuracy).
   - **Code cells** whose output shows the result (see "Cells show, markdown interprets").
   - **A "What we found." markdown cell** that states the finding with the number that decides it
     and, for a hypothesis, the verdict in bold: **Hypothesis N holds / does not hold / is
     supported, not proven.**
5. **Closing sections**: synthesis, limits (what the analysis cannot tell the stakeholder), and the
   deliverable (memo or recap) when the assignment asks for one.

## Cells show, markdown interprets

- A code cell's output is a **chart** (a multi-panel chart when comparing two things) and, where
  exact numbers matter, a **labelled table** (a DataFrame or Series with readable column names; use
  `.rename(columns={...})` at display time). A regression's slope and r go on its chart.
- **Never narrate results in print statements** (`print("share that overstated:", x)`) and then
  interpret them below. A wall of labelled numbers does not show which one matters. Pass/fail checklists are `pd.Series(checks)`.
- Every number the markdown quotes must be **visible in a cell output above it** (a table, a chart
  title or legend, a labelled value). This includes the brief (whose numbers come from the setup
  notebook's last section, after a "**What was observed.**" label), the synthesis, the memo, and the
  recap; `nb_lint.py --trace` checks all of them. The trace only shows that a number appears
  somewhere; read each one against the table it comes from.
- One idea per cell. If a cell needs a paragraph of explanation in the middle, split it.

## Naming

- Rename source columns **once, right after loading**, through one explicit mapping
  (`POLL_NAMES = {"samplesize": "sample_size", "margin_poll": "poll_margin_pts", ...}`), and
  explain the convention in markdown before it.
- lower_snake_case; **the unit in the name** (`poll_margin_pts`, `error_pts`, `earnings_usd`);
  the same quantity has the same name in every file; codes become words (`FM-15` to `routine`).
- Source names appear only where an API or file format requires them.
- Variables in code may be named; **variables never appear in findings, titles, or labels** (see
  `writing-standards`).

## Size

A reader works through the notebook in one sitting. Finished case studies built with these
skills set the scale:
- a setup notebook of about 40 to 60 cells and 150 to 250 lines of code;
- an analysis notebook of about 60 to 75 cells and 200 to 300 lines of code, with 10 to 15 figures;
- opening markdown of three to six sentences; a "What we found" of two to five.
Every data-quality check still runs. Several checks can share one table, and a check that does not
apply is one line. Going well past this scale usually means sections that do not serve the
questions, or code doing more than the lesson needs.

## Code

- Simple enough for a student to read line by line: one-line groupbys; `assign` for new columns; a
  boolean mask with a name (`storm_days = ...`) instead of nested `np.where`; a plain DataFrame built
  from named Series instead of a dictionary comprehension; a code cell of about 15 lines or fewer.
  No clever plumbing the lesson does not need.
- One small helper function only for a chart drawn many times; it takes its data as arguments.
- Colors set where the plot is drawn; **no module-level style constants** (`FOCUS = "#b8432f"`).
- Comments explain **why**, never restate what the line does. `# True counts as 1` earns its place;
  `# group by year` does not. Most cells need no comment because the markdown above explains them.
- Randomness gets a fixed seed (`random_state=0`).
- Raw downloads stay unchanged on disk; cleaning happens in code, so it can be re-run.

## Runs top to bottom

- Restart the kernel and run all before handing over: no errors, no stale outputs, no cell that
  depends on an out-of-order run. `jupyter nbconvert --to notebook --execute --inplace NB.ipynb`.
- Relative paths only; no `os.chdir`, no absolute paths, no machine-specific folders.

## When writing a student version

An instructor may want a version with blanks for students. Write each blank so it fails with
`NameError: name 'FILL_IN' is not defined` (`.agg(FILL_IN)`, `daily[FILL_IN]`), never `___`
(a real IPython variable). Replace "What we found" answers with
"*(your answer, with the number that decides it)*".

## Reference

- `references/examples.md` - weak and strong versions of the same cells, taken from case-study
  drafts.
- `scripts/nb_lint.py` - the automated check for these rules plus the figure and writing rules it
  can detect.
