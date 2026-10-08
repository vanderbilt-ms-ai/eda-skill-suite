---
name: eda-verify
description: Checks an analysis before anyone relies on it, by re-running the notebooks and confirming every number, word, hypothesis, and figure against the data with the suite's tools. Use before handing over any analysis.
---

# Verify

Check the analysis against the data, not against the notebook's own explanation. A notebook can
run without errors and read clearly while its numbers are wrong, and the automated checks catch
only part of that. Each step below says which tool runs it and what a person still has to read.

## 1. Re-run from scratch

`jupyter nbconvert --to notebook --execute --inplace NB.ipynb` for the setup notebook, then the
analysis notebook. No errors, no stale outputs.

## 2. Lint and trace

`python <eda-tools>/scripts/nb_lint.py NB.ipynb --trace` on both notebooks (`eda-tools` says
where the scripts are). Fix every ERROR. Read every WARN and decide it; the wording warnings
("fell as", "a record", "caused", a framing sentence, a cell over 200 words) are flags for a
person, and the trace warnings each need the number found in an output or a figure, or the claim
removed.

## 3. Hypotheses came in the right order

`python <eda-tools>/scripts/check_order.py <project folder>`: `hypotheses.md` predates every file
in `data/raw/`, and the analysis notebook's series A cell matches it verbatim. Then read: every
series B hypothesis names what prompted it, and the thing that prompted it appears earlier in the
notebooks.

## 4. Re-derive the key numbers independently

For each number the conclusions rest on (the verdicts, the synthesis, the memo's evidence), compute
it again in a separate script from the cleaned data, by a different route where possible (a loop
instead of a groupby; counting instead of summing a boolean). Any disagreement is a bug in one of
them; find which.

## 5. The unit of analysis survived

Row counts before and after each filter, join, groupby, and resample. A join that multiplies rows,
a filter that drops a year, or a count of readings reported as a count of periods changes every
number downstream.

## 6. Verdicts

Against `eda-analysis-selection` (The verdict): each hypothesis was tested with the measure its
wording requires, against the size it said matters; each verdict follows from the numbers shown;
no failed hypothesis was repaired with a different measure; every "something else" finding is
supported by its own section's evidence.

## 7. Words

Against `eda-writing-standards`: read the brief, every "What we found", the synthesis, the memo,
and the recap in full. The lint flags some of the wording; the rest (a claim beyond what the record
holds, a figurative phrase, a framing sentence, a fragment) is caught only by reading.

## 8. Gaps and windows

Every measure that depends on continuity was handled as `eda-data-quality` (Gaps in a series)
says, and the findings say how. Every rank names its window.

## 9. Look at every figure

`python <eda-tools>/scripts/figures.py NB.ipynb <out folder>` writes every figure to a PNG. Open
each one: title, labels, ticks, highlight, nothing overlapping, the numbers drawn on it match the
tables.

## Report

Write `verification.md` beside the notebooks: what was run, lint results, the numbers re-derived
(claimed vs re-derived), row counts through the pipeline, problems found and fixed, and anything
left unresolved. Keep it short and factual.
