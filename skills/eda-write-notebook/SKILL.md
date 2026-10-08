---
name: eda-write-notebook
description: Builds an analysis notebook a non-programmer can read and a colleague can re-run: section structure, outputs that show results, column naming, size, and code rules. Use whenever creating, editing, or reviewing a Jupyter notebook for data analysis.
---

# How a notebook is built

**Inputs.** Any notebook in the project, at any stage.

**Produces.** No file of its own. These rules apply to every cell of both notebooks
(`eda-investigate`). The lint in `eda-scripts` checks what a script can check; run it after
editing a notebook.

Two readers decide every rule here. Someone who is not a data scientist reads the markdown and
understands what was asked, what was done, and what was found. A colleague re-runs the code and
gets the same numbers.

## Structure

1. The first cell is the brief (`eda-write-hypotheses`).
2. The setup cell holds imports and the data load, nothing else. Data comes from the files the
   setup notebook wrote, by relative path (`data/...`).
3. One section per step of the investigation, in the order the steps happened, with a `## `
   heading that names the subject: "Hypothesis 1 - Poll error by sample size, 2020", "Digging
   deeper - State error against the state's result, 2012". Someone reading only the headings
   sees the path the investigation took.
4. Each section has three parts, in this order:
   - opening markdown: what the measure is, how the code derives it, why it bears on the
     hypothesis, and what result would refute it. A section that tests a hypothesis opens with
     that hypothesis;
   - code cells whose output shows the result;
   - a "**What we found.**" markdown cell, written after the code has run and from its output,
     with the number that decides the finding and, for a hypothesis, the verdict in bold
     (`eda-test-hypothesis`, section 3).
   A model section adds two parts (`eda-model`, The four parts of a model section).
5. The closing sections: synthesis; limits (what the analysis cannot tell the stakeholder); the
   memo; the recap table (question, hypothesis, what the data showed).

## Cells show, markdown interprets

- A code cell's output is a chart (several panels when comparing two things) and, where exact
  numbers matter, a labelled table: a DataFrame or Series with readable column names, renamed at
  display time with `.rename(columns={...})`. A regression's slope and r go on its chart.
- A print statement that narrates a result (`print("share that overstated:", x)`) with the
  interpretation below it is a breach, because a wall of labelled numbers does not show which one
  matters. A pass/fail checklist is `pd.Series(checks)`.
- Every number the markdown quotes is visible in a cell output above it: a table, a chart title or
  legend, a labelled value. This includes the brief (its numbers come from the setup notebook's
  last section, under a "**What was observed.**" label), the synthesis, the memo, and the recap.
  `nb_lint.py --trace` checks all of them, but it only shows that a number appears somewhere;
  read each one against the table it comes from.
- One idea per cell. A cell that needs a paragraph of explanation in the middle is two cells.

## Naming

- Rename source columns once, right after loading, through one explicit mapping, and explain the
  convention in markdown before it. Example:

  ```python
  # 538's names -> our names. Everything after this cell uses our names.
  POLL_NAMES = {"cycle": "year", "samplesize": "sample_size", "margin_poll": "poll_margin_pts"}
  LOCATION_CODES = {"US": "National", "M1": "ME-1", "M2": "ME-2"}
  ```
- lower_snake_case; the unit in the name (`poll_margin_pts`, `earnings_usd`); the same quantity
  has the same name in every file; codes become words (`FM-15` becomes `routine`).
- Source names appear only where an API or a file format requires them.
- Column names appear in code only. In findings, titles, and labels they are breaches
  (`eda-write-prose`, Words that match the data).

## Size

A reader works through a notebook in one sitting:
- setup notebook: about 50 to 80 cells and 200 to 350 lines of code, with the data-quality
  section inside the budget `eda-check-data` sets;
- analysis notebook: about 60 to 80 cells, 200 to 300 lines of code, 10 to 15 figures;
- markdown lengths as `eda-write-prose` (Length) sets them.

A notebook well past this size usually has sections that do not serve the questions, or code
that does more than the analysis needs.

## Code

- Simple enough for a student to read line by line: one-line groupbys; `assign` for new columns;
  a named boolean mask (`final_week = ...`) instead of nested `np.where`; a DataFrame built from
  named Series; a code cell of about 15 lines or fewer.
- A helper function only for a chart or a calculation repeated many times, taking its data as
  arguments. The download helper is `fetch.py` from `eda-scripts`, not a function written in the
  notebook, so that every project downloads the same careful way.
- Colors are set where the plot is drawn. A module-level style constant puts a choice far from
  where it matters.
- A comment explains why, never what the line does; the markdown above already says what.
- Randomness gets a fixed seed (`random_state=0`).
- Raw downloads stay unchanged on disk; cleaning happens in code, so it can be re-run.

## Runs top to bottom

- Restart the kernel and run all before handing over: no errors, no stale outputs, no cell that
  depends on an out-of-order run. `jupyter nbconvert --to notebook --execute --inplace NB.ipynb`.
- Relative paths only. No `os.chdir`, no absolute paths, no machine-specific folders.

## Student versions

These skills produce the analyst's notebooks. A student version, with blanks, placeholder
findings, and a prediction prompt, is a teaching artifact with its own rules in the course's
case-study skill.

## Reference

- `references/examples.md`: weak and strong versions of the same cells, from case-study drafts.
  Read it when a cell's output or wording is in doubt.
