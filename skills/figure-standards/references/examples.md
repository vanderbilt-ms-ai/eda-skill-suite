# Figures that broke the rules, and the fixes

From case-study drafts, most from the 2020 polls case.

## A bar chart nobody could read

Before: no title; y-axis "Average miss (points)"; x-axis "Sample size" with ticks "smallest",
"small", "large", "largest". A reader could not tell what the bars measured or what separated the
groups.

```python
bar_chart(by_size.index, by_size["abs_error_pts"], "Average miss (points)", xlabel="Sample size")
```

After: a title naming what it shows, an axis label that says the measure, real ranges as ticks.

```python
size_ranges = [f"{low:,.0f} to {high:,.0f}" for low, high in
               zip(by_size["smallest_sample"], by_size["largest_sample"])]
bar_chart(size_ranges, by_size["abs_error_pts"], "2020 polls: average error by sample size",
          "People interviewed (four groups of about 296 polls each)",
          "Average error, either direction (points)")
```

And beside it, the scatter of every poll, because grouped bars hide the individual cases:

```python
ax.scatter(polls_2020["sample_size"], polls_2020["abs_error_pts"], s=10, color="silver")
ax.plot(sizes, fit.params["Intercept"] + per_tenfold * np.log10(sizes), color="firebrick")
ax.set_xscale("log")
ticks = [200, 500, 1000, 2000, 5000, 10000, 50000]
ax.set_xticks(ticks, [f"{t:,}" for t in ticks])
ax.minorticks_off()
ax.set(title=f"2020 polls: each poll's error against its sample size ({len(polls_2020)} polls)\n"
             f"Regression line: {per_tenfold:+.2f} points per tenfold increase | r = {r:.2f}",
       xlabel="People interviewed (log scale)", ylabel="Error, either direction (points)")
```

## A truncated axis

Before: the share of polls that picked the winner, with the y-axis running from 70% to 85%. A
3-point difference looked like a doubling. After: `ylim=(0, 100)`.

## Every other tick

Before: bars for weeks 1 to 9 with ticks only at 2, 4, 6, 8, because the x values were integers and
matplotlib chose the ticks. After: pass the categories as strings (`by_week.index.astype(str)`) so
every bar is labelled.

## Titles colliding

Before: two scatters side by side, each with a two-line title; the titles ran into each other.
After: `plt.subplots(2, 1, figsize=(9, 11))` with `fig.subplots_adjust(hspace=0.45)`.

## A legend on top of the data

Before: a histogram legend in the upper left, over the tallest bar. After: the legend moved to the
empty corner and `ax.set_ylim(top=ax.get_ylim()[1] * 1.3)` added headroom.

## A matched pair that was not matched

Before: the first variable by day as a bar chart, then the second variable as a two-line chart in a
different section, with an unrelated chart between them. After: the second variable as the same bar
chart, same layout, immediately after the first; a third related measure after that, in the same
form.
