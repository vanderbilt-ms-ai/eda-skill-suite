---
name: eda-draw-figure
description: Draws figures that make their point without the analyst in the room, in an analysis notebook, memo, or report. Owns plot choice, titles, labels, integrity, color, highlight, and matched pairs. Use whenever drawing, fixing, or reviewing a chart, including requests that never say "figure standards" such as "plot this" or "why is this chart confusing".
---

# Figure standards

A figure makes its point without the analyst in the room: a reader gets it within about five
seconds. Four principles cover most of what that takes: graphical integrity, keep it simple, use
color sensibly, use the right plot type. The rules below make those concrete and checkable.

After drawing a figure, look at the rendered image (`eda-scripts/scripts/figures.py` writes every
figure in a notebook to PNG). Overlapping titles, a legend over the data, unreadable ticks, and
truncated labels are only visible in the render.

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

- For a numeric predictor, show every observation, not only grouped summaries: a scatter of each
  case with its regression line. Grouped bars may sit beside it, but they hide the cases.
- When comparing one case (a year, a state) against the others, draw them all and highlight the
  one being asked about.
- Matched pairs: when two variables are in play and one is shown in a given form, show the other
  in the same form, adjacent.

## 2. Make it readable without you

- A title on every figure, naming what it shows. During exploration the title names the subject
  ("2020 polls: average error by sample size"); in a memo or report figure it states the finding
  ("Large and small polls missed by the same amount").
- Axis labels in plain language with the unit and, for signed quantities, the direction ("Average
  error (points; above 0 = overstated Biden)"); never a variable name (`eda-write-prose`).
- Real tick values: group bars carry their actual ranges ("138 to 637"), not "small" and "large";
  every bar labelled; log axes show plain numbers (1,000 and 10,000, not 10^3).
- Reference lines are labelled: a threshold the question names, zero, the result, the average.
- The numbers that matter go on the figure: a regression's slope and r in the title's second line;
  an average's value in its legend label.
- Dollar signs: matplotlib reads text between two `$` signs as a formula. Write `\$` or "dollars".
- Nothing overlaps: titles across subplots, a legend over the data, labels over points. Stack
  subplots vertically when titles are long; add headroom (`ax.set_ylim(top=...)`) for a legend.

## 3. Integrity

- Bar charts start at zero. For a quantity whose zero means nothing (a temperature in degrees F, a
  year), do not use bars: use a dot plot or a line, or bars of the difference from a labelled
  baseline.
- Same axes when two panels are meant to be compared.
- Do not smooth, bin, or aggregate away the thing the question is about; say in the markdown what
  the simplification dropped.
- Point counts and sample sizes are visible somewhere (title, legend, or the table beside it).

## 4. Color

- Choose by what the data is doing: qualitative (categories), sequential (low to high), diverging
  (above and below a midpoint), highlight (one case against the rest).
- Highlight: one strong color (for example firebrick) for the case asked about, silver or grey for
  the rest; the figure says what the highlight means. Keep the same color meaning everywhere in
  the notebook.
- Colorblind-safe palettes for categories; never red against green as the only distinction.
- Set colors where the plot is drawn, not as module-level constants.

## 5. Describe it

In the markdown after the figure, the reader can complete the five-step figure description: the
topic, what the y-axis shows, what the x-axis shows, what each point, line, or bar therefore
represents, and the takeaway. If any step is unclear from the figure, fix the figure. The takeaway
belongs in "What we found", stated with its number.

## Reference

- `references/examples.md`: three figures that meet every rule and three that break at least one,
  with images and a rule-by-rule check. All six are from one case (the 2020 polls); they show the
  rules, they do not extend them.
