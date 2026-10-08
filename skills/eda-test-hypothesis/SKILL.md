---
name: eda-test-hypothesis
description: Chooses the analysis and figure that test a hypothesis as worded, states the verdict, and writes the next hypothesis. Owns the verdict rules. Use whenever a claim or question needs testing against data.
---

# Choosing the analysis and stating the verdict

A test answers the claim as it is worded; a test of a different measure answers a different
question. This skill picks the analysis that answers the claim, states the verdict, and turns the
next question into the next hypothesis. It owns the verdict rules; the hypothesis form is in
`eda-write-hypotheses`, Hypotheses.

## 1. Read the claim exactly

Write down, in the section's opening markdown:
- The claim, quoted from the hypothesis (series A or B).
- The comparison it implies: compared with what, on the same kind of case, over the same window?
- The measure the wording requires: a claim about a period is tested with the period's own numbers
  (its total, its average, its most extreme value); a claim about one day with daily numbers.
- The unit and window: the same days across years; the case's own period excluded from its
  baseline. A rank holds only for its window; say whether a longer record is available and
  whether it would change the rank.
- The variable classes: continuous or discrete numeric; nominal, ordinal, or binary categorical;
  time.
- "Refuted if" and the size that matters, copied from the hypothesis. Do not change them here.

## 2. Choose the analysis

| The claim says | Analysis | Figure |
|---|---|---|
| X was unusual or extreme | the same measure for every comparable case; the case's rank; the gap to the next case | one bar per case, the case highlighted |
| group A differs from group B | split-apply-combine: the summary per group, with the count per group | bars of the summary; box plots when spread matters |
| Y rises or falls with X (two numeric) | scatter plus a regression line: slope in the data's units, r, R-squared; a log scale when X spans orders of magnitude | scatter with the line |
| Y differs by category after accounting for X | multiple regression; compare R-squared with and without each block of variables | bars of R-squared by model; a table of coefficients |
| events concentrate in time | the series at a finer grain (month, then day, then hour); resample irregular readings first | bars by day; a line by hour |
| something lasted or accumulated | duration past a threshold; the longest unbroken run; a cumulative sum, with gaps handled as `eda-check-data` says | cumulative line, every case drawn, the case highlighted |
| a combination of conditions explains it | how many cases meet each condition alone, and how many meet all | scatter of the two conditions with threshold lines |
| there are kinds of cases | clustering; hand to `eda-model` | scatter colored by cluster |
| we could have told in advance | a rule or classifier evaluated on every case, with the cases it misses; hand to `eda-model` | scatter with thresholds; confusion matrix |
| this pattern explains the event | the same analysis where the event did not happen (other years, other groups) | the same chart for the comparison case, adjacent |

The figure rules (every observation shown for a numeric predictor, the highlight, matched pairs,
titles and labels) are in `eda-draw-figure`.

## 3. Run it, then state the verdict

- Show the chart and a labelled table with the numbers the verdict rests on.
- The verdict, in bold, as worded: **Hypothesis N holds**, **does not hold**, or **is supported,
  not proven** (the evidence fits but cannot rule out the alternatives, or the test was tuned on
  the case it flags). "Partly holds" and "depends on the measure" are not verdicts.
- A difference in the claimed direction that is smaller than the size the hypothesis said matters
  is **does not hold**, with both numbers stated.
- A result exactly on the refutation line is decided by the refutation as written ("refuted if
  fewer than three": three holds). State the result and the line together.
- A failed hypothesis stays failed. A different measure that "works" is a new series B
  hypothesis that exists because this one failed; it is not a repair of this one.
- If the data cannot test the claim as worded, say so, and offer the closest test as a series B
  hypothesis.

*The analyst decides* whether the test matches the claim, and the verdict.

## 4. The next hypothesis

End the section with the next question, chosen from the moves in `eda-investigate` (Where the next
question comes from), and write it as a series B hypothesis with its refutation. Each
digging-deeper step is its own section with its own chart, opened by the hypothesis it tests.

*The analyst decides* which hypothesis comes next.

## Reference

- `references/worked-choices.md`: claims from case studies and the analysis each one needed,
  including the ones first tested the wrong way.
