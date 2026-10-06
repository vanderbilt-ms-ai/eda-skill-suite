---
name: figure-standards
description: The rules every figure in an analysis follows - choosing the plot type from the variables and the question, graphical integrity, color, and a figure a reader can understand without anyone standing next to it - a title, plain-language axis labels with units and direction, real tick values, labelled reference lines, no overlaps, and the five-step figure description. Use this skill whenever you draw, fix, or review a chart in a notebook or report, including when another EDA skill asks for a figure, even if the request only says "plot this".
---

# Figure standards

A figure has to make its point without the analyst in the room: a reader should get it within
about five seconds. Four principles cover most of what that takes: **graphical integrity, keep it
simple, use color sensibly, use the right plot type.** The rules below make those concrete.

After drawing a figure, look at the rendered image (in the notebook, or saved to PNG and opened).
Overlapping titles, a legend over the data, unreadable ticks, and truncated labels are only visible
in the render.

## 1. Choose the plot type from the variables and the question

| The question is about | Variables | Plot |
|---|---|---|
| change over time | one numeric over a time axis | line |
| the distribution of one variable | one numeric | histogram (box plot to compare several) |
| one summary per group | categorical + one statistic | bar |
| distributions across groups | categorical + numeric | box plot, or overlaid histograms |
| how two numeric variables move together | two numeric | scatter, with a regression line when you fit one |
| a matrix of values | two categorical or two binned numeric + a value | heatmap |
| many numeric variables at once | many numeric | correlation heatmap, pair plot, or a reduction (principal components) |

- **For a numeric predictor, show every observation**, not only grouped summaries: a scatter of
  each case with its regression line. Grouped bars may sit beside it, but they hide the cases.
- When comparing one case (a year, a state) against the others, draw them all and **highlight the
  one being asked about** (one strong color, the rest grey).
- When two variables are in play and you show one in a given form, show the other in the same form,
  adjacent (the first variable by day, then the second variable by day, as the same kind of chart).

`eda-analysis-selection` makes this choice as part of choosing the analysis; this table is its
source.

## 2. Make it readable without you

- **A title on every figure, naming what it shows**: "2020 polls: average error by sample size",
  "2020 state polls: error against the state's result". During exploration the title names the
  subject; in a report or memo figure the title states the finding ("Large and small polls missed
  by the same amount").
- **Axis labels in plain language with the unit and, for signed quantities, the direction**:
  "Average error (points; above 0 = overstated Biden)", "Temperature (degrees F)". Never a variable
  name (`abs_error_pts`, `pts`).
- **Real tick values**: group bars carry their actual ranges ("138 to 637"), not "small" and
  "large"; every bar labelled; log axes show plain numbers (1,000 and 10,000, not 10^3).
- **Reference lines are labelled**: a threshold the question names, zero error, the result, the average.
- **The numbers that matter go on the figure**: a regression's slope and r in the title's second
  line; an average's value in its legend label.
- **Dollar signs**: matplotlib reads text between two `$` signs as a formula and drops the signs.
  Write `\$` in titles, labels, and annotations, or write "dollars".
- **Nothing overlaps**: titles across subplots, a legend over the data, labels over points. Stack
  subplots vertically when titles are long; add headroom (`ax.set_ylim(top=...)`) for a legend.

## 3. Integrity

- **Bar charts start at zero.** Truncating a bar axis exaggerates differences. For a quantity
  whose zero means nothing (a temperature in degrees F, a year), do not use bars: use a dot plot or
  a line, or bars of the difference from a labelled baseline (the average).
- Same axes when two panels are meant to be compared.
- Do not smooth, bin, or aggregate away the thing the question is about; say in the markdown what
  the simplification dropped (Tukey: simplify, and notice where the lying happens).
- Point counts and sample sizes are visible somewhere (title, legend, or the table beside it).

## 4. Color

- Choose by what the data is doing: **qualitative** (categories), **sequential** (low to high),
  **diverging** (above and below a midpoint), **highlight** (one case against the rest).
- Highlight: one strong color (for example firebrick) for the case asked about, silver or grey for
  the rest. Keep the same color meaning everywhere in the notebook.
- Colorblind-safe palettes for categories; never red against green as the only distinction.
- Set colors where the plot is drawn, not as module-level constants.

## 5. Describe it

In the markdown after the figure, the reader should be able to complete a five-step figure
description: **(1) the topic, (2) what the y-axis shows, (3) what the x-axis shows, (4) what each
point, line, or bar therefore represents, (5) the takeaway.** If any step is unclear from the
figure, fix the figure. The takeaway belongs in "What we found", stated with its number.

## Reference

- `references/examples.md` - figures from the finished case studies that broke these rules, and
  their fixes.
