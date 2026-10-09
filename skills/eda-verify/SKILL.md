---
name: eda-verify
description: Checks a finished analysis against the data before anyone relies on it, by re-running both notebooks and confirming every number, word, hypothesis, and figure. Use before handing over any analysis notebook or memo.
---

# Verifying the analysis against the data

**Inputs.** The project folder: both notebooks, `hypotheses.md`, `hypotheses.stamp`, `data/`, and
`decisions.md`.

**Produces.** `verification.md` in the project folder, and the fixes made along the way. Each
step below names the script that runs it and what a person still reads, because a notebook can
run without errors and read clearly while its numbers are wrong, and a script catches only part of
that.

## 1. Re-run both notebooks from scratch

```bash
jupyter nbconvert --to notebook --execute --inplace <case>-step0-get-the-data.ipynb
jupyter nbconvert --to notebook --execute --inplace <case>-analysis.ipynb
```

No errors, no stale outputs.

## 2. Run the lint and the number trace

`python <eda-scripts>/scripts/nb_lint.py NB.ipynb --trace` on both notebooks. Fix every ERROR.
Read every WARN and decide it. The wording warnings ("fell as", "a record", "caused", a framing
sentence, a cell over 200 words) are candidates for a person to judge. Each trace warning is a
quoted number that no output shows: find it in an output or on a figure, or remove the claim.

## 3. Check that the first hypotheses came before the data

`python <eda-scripts>/scripts/check_order.py <project folder>`. It checks that `hypotheses.md`
is unchanged since its stamp, that every file in `data/raw/` is newer than the stamp, and that
the analysis notebook holds the file verbatim. Then read the second-set hypotheses: each names
what prompted it, and the prompting table or finding appears earlier in the notebooks.

## 4. Re-derive the key numbers

For each number the conclusions rest on (every verdict, the synthesis, the memo's evidence),
compute it again in a separate script from the clean data, by a different route where one exists:
a loop instead of a groupby, a count instead of a sum of booleans. A disagreement is a bug in one
of the two; find which.

## 5. Check that the unit of analysis survived

Record row counts before and after each filter, join, groupby, and resample. A join that
multiplies rows, a filter that drops a year, or a count of readings reported as a count of hours
changes every number after it.

## 6. Check the verdicts

Against `eda-test-hypothesis` (section 3): each hypothesis was tested with the measure its wording
requires and against the size it named; each verdict follows from the numbers shown; no failed
hypothesis was re-tested with a different measure under the same number; every claim in the
"something else" section is supported by that section's own evidence.

## 7. Read the words

Against `eda-write-prose`: read the brief, every "What we found", the synthesis, the memo, and
the recap in full. The lint flags some wording; a claim beyond what the record holds, an idiom, a
framing sentence, or a fragment is caught only by reading.

## 8. Check gaps and periods

Every measure that depends on continuity was computed as `eda-check-data` (Gaps in a series)
says, and the finding says which way. Every rank names the years it was computed over.

## 9. Look at every figure

`python <eda-scripts>/scripts/figures.py NB.ipynb <out folder>` writes every figure to a PNG.
Open each one and check the title, the labels, the ticks, the highlight, that nothing overlaps,
and that the numbers drawn on it match the tables.

## The report

Write `verification.md` beside the notebooks with: what was run; the lint results; each
re-derived number (claimed, re-derived); the row counts through the pipeline; the problems found
and fixed; anything unresolved. Keep it to the facts.
