# Worked choices

Claims, the analysis each needed, and the mistakes made first. Each entry names its case; the
entries in brackets are the general pattern with the case left out. They are examples of the rules
in `SKILL.md`, not rules of their own.

## "Small samples caused the polling error: polls with larger samples missed by less." (2020 polls)

- Variables: sample size (continuous, 138 to 50,908) and error size (continuous).
- Analysis: the scatter of every poll's error against its sample size on a log scale, with a
  regression line (slope per tenfold increase, r); grouped means by sample-size quartile beside it.
- Mistake made first: only the quartile bars, with "smallest" to "largest" as tick labels. The
  groups hid the individual polls and the ticks hid the ranges.

## "The error depended on where a poll was taken, not on how it was run." (2020 polls)

- Analysis: three regressions of each poll's error: on how it was run (sample size, phone or not,
  days before the election), on where (the state's result), on both; compared by R-squared.
- Figure: bars of R-squared for the three models.

## "The state pattern explains why this election was different." (2020 polls)

- This claim needs the same analysis where the event did not happen: the regression of state error
  on the state's result for 2012, an election the polls did not miss in that direction.
- What it found: the same slope in 2012 and in every election since 2000. The slope was normal;
  what moved in 2016 and 2020 was the line's level. Without the comparison, the slope would have
  been reported as the cause.

## "[This period] was [more extreme] than [the same period in other years]." (pattern; from the ice storm)

- Comparison: one period against the same calendar window in every other year pulled.
- Measure the wording requires: the period's own number (its total, its average, its most extreme
  value), not one day inside it.
- Analysis: that number per year; the case's rank with its window ("4th of 30"); the average of
  the other years.
- Figure: one bar per year, the case highlighted, the average as a labelled line.
- Mistake made first: calling the claim "partly true" because one day inside the period was
  extreme. The single day is a different measure; after the claim fails it becomes a series B
  hypothesis.

## "[Something] lasted longer than usual." (pattern; from the ice storm)

- Irregular readings mean counting rows does not count periods: resample first
  (`eda-check-the-data`, What a row is).
- Analysis: periods past the threshold per year in the same window; the longest unbroken run; the
  cumulative count.
- Gaps are handled as `eda-check-the-data` (Gaps in a series) says, and the finding says which way.
- Figure: cumulative count past the threshold, one line per year, the case highlighted.

## "A single number we already track would have flagged it." (pattern; from the ice storm)

- Analysis: apply the threshold to every period in every year; count what it flags besides the
  case.
- Figure: every period as a point, the threshold as a labelled line, the case highlighted.
- Caution: a threshold chosen after seeing the case will flag the case; test it on years not used
  to choose it, or say it is untested (`eda-model`, Overfitting check).

## "Paying more pays off." (pattern; from College Scorecard)

- The words name a comparison of gain against cost, not only "more is associated with more".
- Analysis: the gain per unit of cost (a slope), the cost the gain has to recover, and the time or
  amount needed to recover it.
- Refuted if: the gain does not recover the cost within a horizon the stakeholder would accept,
  set before looking.
