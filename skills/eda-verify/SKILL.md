---
name: eda-verify
description: Verify a finished or in-progress analysis notebook before anyone relies on it - re-run it from a fresh kernel, lint it against the notebook, figure, and writing standards, trace every number in the findings, memo, and recap to an output, re-derive the key numbers independently from the data, confirm the unit of analysis survived every step, check that each hypothesis was tested as worded and each verdict follows, check the wording against what the data recorded, and look at every figure. Use this skill before handing over any analysis, after another skill or an AI assistant wrote notebook cells, or whenever someone asks to check, review, or verify an analysis.
---

# Verify

Check the analysis against the data, not against the notebook's own explanation. A notebook that
an assistant wrote can run without errors and read clearly while its numbers are wrong; the checks
below are how that is caught.

## 1. Re-run from scratch

`jupyter nbconvert --to notebook --execute --inplace NB.ipynb` for the setup notebook, then the
analysis notebook. No errors, no stale outputs.

## 2. Lint

`python ../notebook-standards/scripts/nb_lint.py NB.ipynb --trace` on both notebooks. Fix every
ERROR. For each trace WARN, find the number in an output (or, for a number drawn inside a figure,
in the figure itself); if it is nowhere, it is unsupported. The trace covers the brief, every
"What we found", the synthesis, the memo, and the recap.

## 3. Re-derive the key numbers independently

For each number the conclusions rest on (the verdicts, the synthesis, the memo's evidence), compute
it again in a separate scratch script from the cleaned data, by a different route where possible
(a loop instead of a groupby; counting instead of summing a boolean). Any disagreement is a bug in
one of them; find which.

## 4. The unit of analysis survived

Row counts before and after each filter, join, groupby, and resample. A join that multiplies rows,
a filter that drops a year, or a count of readings reported as a count of hours changes every
number downstream.

## 5. The hypotheses and verdicts

- The hypotheses and their refutations are the ones written before the data was pulled; any
  changed later is labelled a new question.
- Each hypothesis was tested with the measure its wording requires, against the size of difference
  it said matters.
- Each verdict follows from the numbers shown; none was rescued with a different measure.
- Every "something else" finding is supported by its own section's evidence.

## 6. The words match the data

Using `writing-standards`: "reported" not "fell as"; "the most in eleven years" not "a record"; "not
recorded" not "did not happen"; association not causation; no aphorisms; no variable names in
findings, titles, or labels.

## 7. Gaps and windows

- Every measure that depends on continuity (runs, durations, cumulative counts) was checked for
  gaps in the series, and the findings say how gaps were handled.
- Every rank and "the most in N" names its window.

## 8. Look at every figure

Extract or open every figure and look: title, labels, ticks, highlight, nothing overlapping, the
numbers drawn on it match the tables.

## Report

Write `verification.md` beside the notebooks: what was run, lint results, the numbers re-derived
(claimed vs re-derived), row counts through the pipeline, problems found and fixed, and anything
left unresolved. Keep it short and factual.
