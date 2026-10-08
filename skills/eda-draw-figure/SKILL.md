---
name: eda-draw-figure
description: Draws a chart that makes its point without the analyst present, for an analysis notebook, memo, or report. Use whenever drawing, fixing, or reviewing a chart, including requests such as "plot this" or "why is this chart confusing".
---

# How a figure is drawn

**Inputs.** The data for one chart, and the hypothesis or question the chart serves.

**Produces.** One figure in a notebook cell, and the markdown after it. A reader should understand
the figure within about five seconds, because a figure in a memo is read without the analyst in
the room.

After drawing, look at the rendered image. `figures.py` in `eda-scripts` writes every figure in a
notebook to a PNG. Overlapping titles, a legend over the data, unreadable ticks, and cut-off
labels show only in the render.

## 1. Choose the plot from the variables and the question

| The question is about | Variables | Plot |
|---|---|---|
| change over time | one numeric over a time axis | line |
| the distribution of one variable | one numeric | histogram; box plots to compare several |
| one summary per group | categorical and one statistic | bar |
| distributions across groups | categorical and numeric | box plots, or overlaid histograms |
| how two numeric variables move together | two numeric | scatter, with a regression line when one is fitted |
| a matrix of values | two categorical, or two binned numeric, and a value | heatmap |
| many numeric variables at once | many numeric | correlation heatmap, pair plot, or principal components |

- For a numeric predictor, draw every observation: a scatter of each case with its regression
  line. Grouped bars may sit beside it, but on their own they do not show the cases.
- When one case (a year, a state) is compared with the others, draw them all and highlight the
  one being asked about.
- Matched pairs: when two variables are in play and one is drawn in a given form, draw the other
  in the same form, immediately after it. The reader compares them by eye.

## 2. Make it readable without you

- A title on every figure that names what it shows. During exploration the title names the
  subject: "2020 polls: average error by sample size". In a memo or report the title states the
  finding: "Large and small polls missed by the same amount".
- Axis labels in plain words with the unit and, for a signed quantity, the direction: "Average
  error (points; above 0 = overstated Biden)". A column name on an axis is a breach.
- Real tick values: grouped bars carry their actual ranges ("138 to 637"), not "small" and
  "large"; every bar labelled; a log axis shows plain numbers (1,000 and 10,000, not 10^3).
- Reference lines labelled: a threshold the question names, zero, the result, the average.
- The numbers that matter on the figure: a regression's slope and r in the title's second line;
  an average's value in its legend label; a count of cases in the title or the table beside it.
- Dollar signs: matplotlib reads text between two `$` signs as a formula. Write `\$` or
  "dollars".
- Nothing overlaps: titles across subplots, a legend over the data, labels over points. Stack
  subplots vertically when titles are long; add headroom for a legend with `ax.set_ylim(top=...)`.

## 3. Integrity

- Bar charts start at zero; a truncated bar axis exaggerates differences. For a quantity whose
  zero means nothing (a temperature in degrees F, a year), do not use bars: use a dot plot, a
  line, or bars of the difference from a labelled baseline.
- Panels meant to be compared share their axes.
- Do not smooth, bin, or aggregate away the thing the question is about. Say in the markdown
  what a simplification dropped.

## 4. Color

- Choose by what the data is doing: qualitative for categories; sequential for low to high;
  diverging for above and below a midpoint; a highlight for one case against the rest.
- Highlight: one strong color (firebrick, for example) for the case asked about, silver or grey
  for the rest, and a label on the figure states what the highlight means. The same color keeps the same
  meaning throughout the notebook.
- Colorblind-safe palettes for categories; never red against green as the only distinction.
- Set colors where the plot is drawn, not as module-level constants (`eda-write-notebook`).

## 5. Describe it

In the markdown after the figure, the reader can answer five things from the figure alone: the
topic; what the y-axis shows; what the x-axis shows; what each point, line, or bar therefore
represents; and the takeaway. If any of the five is unclear from the figure, fix the figure. The
takeaway goes in "What we found", with its number.

## Reference

- `references/examples.md`: three figures that meet every rule and three that break at least one,
  with images and a rule-by-rule check. All six are from the 2020 polls case. Read it when a
  figure is being reviewed.
