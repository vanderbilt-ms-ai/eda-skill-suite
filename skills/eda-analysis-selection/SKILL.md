---
name: eda-analysis-selection
description: Chooses the analysis and figure that test a hypothesis as worded, states the verdict, and proposes the next question. Use whenever a claim or question needs testing against data.
---

# Choosing the analysis and the figure

A test has to answer the claim as it is worded; a test of a different measure answers a different
question. This skill picks the
analysis that answers the claim, says in advance what would refute it, and keeps a failed
hypothesis failed.

## 1. Read the claim exactly

Write down, in the section's opening markdown:
- **The claim**, quoted from the hypotheses.
- **The comparison it implies**: compared with what? ("the polls missed by more in 2020 than in
  2012" compares one election against another, on the same kind of poll and the same final weeks.)
- **The measure the wording requires**: a claim about the month is tested with monthly numbers
  (total, average, most extreme value of the month); a claim about one day with daily numbers.
- **The unit and window**: same days across years; the case's own period excluded from its
  baseline.
- **The variable classes**: continuous or discrete numeric; nominal, ordinal, or binary
  categorical; time.
- **Refuted if**: copied from the hypotheses section, where it was written before any data was
  pulled, including the smallest difference that matters for the decision. Do not change it here.
- **The window**: the years or cases the comparison uses. A rank holds only for its window ("third
  of eleven Januaries"); say whether a longer record is available and whether it would change the
  rank.

## 2. Choose the analysis

| The claim says | Analysis | Figure (see `figure-standards`) |
|---|---|---|
| X was unusual or extreme | the same measure for every comparable case; the case's rank; the gap to the next case | bar chart, one bar per case, the case highlighted |
| group A differs from group B | split-apply-combine: the summary (mean, median, share) per group, with the count per group | bar chart of the summary; box plot when spread matters |
| Y rises or falls with X (two numeric) | scatter plus a regression line: slope in the data's units, r, R-squared; a log scale when X spans orders of magnitude | scatter with the line; grouped bars beside it are optional |
| Y differs by category after accounting for X | multiple regression; compare R-squared with and without each block of variables | bar chart of R-squared by model; table of coefficients |
| events concentrate in time | the series at a finer grain (month, then day, then hour); resample irregular readings first | bar chart by day; line chart by hour |
| something lasted or accumulated | duration below or above a threshold; the longest unbroken run; a cumulative sum | cumulative line chart, every case drawn, the case highlighted |
| a combination of conditions explains it | how many cases meet each condition alone, and how many meet all | scatter of the two conditions with threshold lines |
| there are kinds of cases | clustering - hand to `eda-lens` | scatter colored by cluster |
| we could have told in advance | a rule or classifier evaluated on every case, with the cases it misses - hand to `eda-lens` | scatter with thresholds; confusion matrix |
| this pattern explains the event | the same analysis where the event did not happen (other years, groups) | the same chart for the comparison case, adjacent |

For a numeric predictor, always show every observation (the scatter), even when a grouped summary
is easier to read.

## 3. Run it, then state the verdict

- Show the chart and a labelled table with the numbers the verdict rests on.
- **Verdict as worded**: holds, does not hold, or supported but not proven. If the claim fails,
  it fails. A difference in the claimed direction that is smaller than the size the hypothesis said
  matters is **does not hold**, with both numbers stated. A different measure that "works" is a **new question** that exists because the
  hypothesis failed (the largest single day after a claim about the month's total failed), not a
  rescue.
- If the data cannot test the claim as worded, say so, and offer the closest test labelled as a
  different question.

*The analyst decides* whether the test matches the claim, and the verdict.

## 4. When the obvious explanation fails: the next question

End the section with the next question, chosen from the moves in `eda-workflow` ("Digging deeper:
where the next question comes from"). Each digging-deeper step is its own section with its own
chart. When two variables are in play, build each view for both,
as adjacent pairs in the same form.

*The analyst decides* which question comes next.

## Reference

- `references/worked-choices.md` - claims from case studies and the analysis each one
  needed, including the ones first tested the wrong way.
