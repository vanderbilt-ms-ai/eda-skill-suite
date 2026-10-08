---
name: eda-test-hypothesis
description: Chooses the analysis and figure that test one hypothesis as it is worded, states the verdict, and writes the next hypothesis. Use whenever a hypothesis is ready to be tested against data.
---

# Testing one hypothesis

**Inputs.** One hypothesis, written as `eda-write-hypotheses` requires, and the clean data the
setup notebook saved.

**Produces.** One section of the analysis notebook: the opening markdown, the code, the chart and
table, the "What we found" cell with the verdict, and the next hypothesis. The section's shape is
in `eda-write-notebook` (Structure); the figure rules are in `eda-draw-figure`.

## 1. Read the claim exactly

Write in the opening markdown:
- the claim, quoted from the hypothesis;
- the comparison it implies: compared with what, on the same kind of case, over the same period;
- the measure the wording requires: a claim about a month is tested with the month's total,
  average, or most extreme value, not with one day inside it; a claim about one day with that
  day's values;
- the unit and the period: the same days across years; the case's own period left out of the
  baseline it is compared with. A rank holds only for the years compared; say whether a longer
  record exists and whether it would change the rank;
- the kind of each variable: continuous or discrete numeric; nominal, ordinal, or binary
  categorical; time;
- "Refuted if" and the smallest difference that matters, copied from the hypothesis. Do not change
  them here.

## 2. Choose the analysis

| The claim says | Analysis | Figure |
|---|---|---|
| X was unusual or extreme | the same measure for every comparable case; the case's rank; the gap to the next case | one bar per case, the case highlighted |
| group A differs from group B | the summary (mean, median, share) per group, with the count per group | bars of the summary; box plots when the spread matters |
| Y rises or falls with X (both numeric) | scatter and a regression line: slope in the data's units, r, R-squared; a log scale when X spans orders of magnitude | scatter with the line |
| Y differs by category after accounting for X | multiple regression; R-squared with and without each block of variables | bars of R-squared by model; a table of coefficients |
| events concentrate in time | the series at a finer level of detail: month, then day, then hour; resample irregular readings first | bars by day; a line by hour |
| something lasted or accumulated | duration past a threshold; the longest unbroken run; a cumulative sum, with gaps handled as `eda-check-data` (Gaps in a series) says | a cumulative line per case, the case highlighted |
| a combination of conditions explains it | how many cases meet each condition alone, and how many meet all | scatter of the two conditions with threshold lines |
| there are kinds of cases | clustering (`eda-model`) | scatter colored by cluster |
| it could have been told in advance | a rule or classifier evaluated on every case, with the cases it misses (`eda-model`) | scatter with thresholds; confusion matrix |
| this pattern explains the event | the same analysis where the event did not happen: other years, other groups | the same chart for the comparison case, beside it |

## 3. Run it and state the verdict

- Show the chart and a labelled table with the numbers the verdict rests on.
- Write the verdict in bold, as one of three: **Hypothesis N holds**; **Hypothesis N does not
  hold**; **Hypothesis N is supported, not proven** (the evidence fits, but the alternatives
  cannot be ruled out, or the test was chosen after seeing the case it flags). "Partly holds" and
  "depends on the measure" are not verdicts.
- A difference in the claimed direction that is smaller than the size the hypothesis named is
  **does not hold**. State both numbers.
- A result exactly on the refutation line is decided by the refutation as written: "refuted if
  fewer than three" means three holds. State the result and the line together.
- A hypothesis that does not hold stays that way. A different measure on which the claim would
  hold is a new hypothesis in the second set (`eda-write-hypotheses`), written because this one
  failed. It does not change this verdict.
- If the data cannot test the claim as worded, say so, and write the closest testable claim as a
  new hypothesis.

*The analyst decides* whether the test matches the claim, and the verdict.

## 4. The next hypothesis

End the section with the next question, chosen as `eda-investigate` (Where the next hypothesis
comes from) describes, written as a hypothesis with its refutation. The section that tests it
opens with that hypothesis and has its own chart.

*The analyst decides* which hypothesis comes next.

## Reference

- `references/worked-choices.md`: claims from finished cases, the analysis each needed, and the
  mistake made first.
