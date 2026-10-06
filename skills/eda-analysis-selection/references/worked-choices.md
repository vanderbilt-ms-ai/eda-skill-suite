# Worked choices

Claims, the analysis each needed, and the mistakes made first. The polls entries come from the 2020
polls case; the others are patterns with the case left out.

## "Small samples caused the 2020 polling error: polls with larger samples missed by less."

- Variables: sample size (continuous, spanning 138 to 50,908) and error size (continuous).
- Analysis: the scatter of every poll's error against its sample size on a log scale, with a
  regression line (slope per tenfold increase, r); grouped means by sample-size quartile beside it.
- Mistake made first: only the quartile bars, with "smallest/small/large/largest" as tick labels.
  The groups hid the individual polls and the ticks hid the ranges.

## "The error depended on where a poll was taken, not on how it was run."

- Analysis: three regressions of each poll's error - on how it was run (sample size, phone or not,
  days before the election), on where (the state's result), on both - compared by R-squared.
- Figure: bar chart of R-squared for the three models.

## "The state pattern explains why 2020 was different."

- This claim needs the same analysis **where the event did not happen**: the regression of state
  error on the state's result for 2012, an election the polls did not miss in that direction.
- What it found: the same slope in 2012 (and in every election since 2000). The slope was normal;
  what moved in 2016 and 2020 was the line's level. Without the comparison, the slope would have
  been reported as the cause.

## "[This period] was [more extreme] than [the same period in other years]."

- Comparison: one period against the same calendar window in every other year pulled.
- Measure the wording requires: a claim about the period is tested with the period's own number
  (its total, its average, its most extreme value), not with one day inside it.
- Analysis: that number per year; the case's rank, with the window ("4th of 30"); the average of
  the other years.
- Figure: bar chart, one bar per year, the case highlighted, the average as a labelled line.
- Mistake made first: calling the claim "partly true" because one day inside the period was
  extreme. The single day is a different measure; it becomes the next question after the claim
  fails.

## "[Something] lasted longer than usual."

- Irregular readings (several report types, uneven spacing) mean counting rows does not count
  hours. Choose the representative reading for each hour, resample to one value per hour, and say
  which readings were used.
- Analysis: hours past the threshold per year in the same window; the longest unbroken run; the
  cumulative count by hour.
- **Gaps**: a missing hour inside a run ends it unless handled. Report the run both ways (the gap
  breaks it; the gap filled when the readings on both sides are past the threshold), and say which
  one the findings use.
- Figure: cumulative hours past the threshold, one line per year, the case highlighted.

## "A single number we already track would have flagged it."

- Analysis: apply a threshold to every day in every year, count what it flags besides the case.
- Figure: every day as a point (jittered by year), the threshold as a labelled line, the case
  highlighted.
- Caution: a threshold chosen after seeing the case will flag the case; test it on years not used
  to choose it, or say it is untested.

## "Paying more pays off."

- The words name a comparison of gain against cost, not only "more is associated with more".
- Analysis: the gain per unit of cost (a slope), and the cost the gain has to recover; the time or
  amount needed to recover it.
- Refuted if: the gain does not recover the cost within a horizon the stakeholder would accept,
  set before looking.
