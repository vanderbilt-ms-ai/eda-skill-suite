# Weak and strong cells

Each pair is the same step of an analysis. The weak version is what an assistant tends to write;
the strong version is what the finished case studies do.

## A result narrated in print statements

WEAK - the output is a wall of labelled numbers, and the reader has to assemble the comparison:

```python
national = polls_2020[polls_2020["location"] == "National"]
print(len(national), "national polls")
print("average poll margin:", round(national["poll_margin_pts"].mean(), 1),
      "| result:", round(national["result_margin_pts"].iloc[0], 1))
print("share that overstated Biden:", round((national["error_pts"] > 0).mean(), 2))
```

STRONG - a chart shows the comparison, and a labelled table carries the exact numbers:

```python
fig, (left, right) = plt.subplots(1, 2, figsize=(13, 4))
left.hist(national["poll_margin_pts"], bins=20, color="silver")
left.axvline(result, color="black", linewidth=2, label=f"result: Biden +{result:.1f}")
left.axvline(average_poll, color="firebrick", linestyle="--", linewidth=2,
             label=f"average poll: Biden +{average_poll:.1f}")
left.set(title="2020 national polls: Biden's lead in each poll",
         xlabel="Biden's lead in the poll (points)", ylabel="Number of polls")
left.legend(loc="upper right")
...
pd.DataFrame({"polls": [len(national), len(state_2020)],
              "average error (points)": [national["error_pts"].mean(), average_state_error],
              "share that overstated Biden": [...]},
             index=["national", "state"]).round(2)
```

## A section with no explanation before the test

WEAK:

> ## Hypothesis 1 - Poll error by sample size, 2020
>
> Split the 2020 polls into four equal groups by sample size, and compare how far each group missed.

STRONG - what the measure is, how it is derived, why it bears on the hypothesis, what result would
support it:

> ## Hypothesis 1 - Poll error by sample size, 2020
>
> A poll's **sample size** is the number of people it interviewed. A poll reaches only a sample of
> voters, so even a well-run poll is off by chance, and that chance error shrinks as the sample
> grows: a poll of 400 people has a margin of error of about plus or minus 5 points on each
> candidate's share, a poll of 1,600 about plus or minus 2.5. If small samples caused the 2020
> error, polls with larger samples should have missed by less.
>
> To compare, sort the 2020 polls by sample size and cut them into four groups holding the same
> number of polls (quartiles, with `pd.qcut`). **If the hypothesis holds, the bars fall from left
> to right.**

## A finding without its number or verdict

WEAK: "Sample size doesn't really seem to matter much."

STRONG: "The quarter of polls with the smallest samples (138 to 637 people) missed by 5.2 points
on average; the quarter with the largest (1,205 to 50,908) missed by 5.1. ... **Hypothesis 1 does
not hold:** sample size does not explain the 2020 error."

## Column names

WEAK - source names survive into the analysis, half renamed:

```python
polls = raw.rename(columns={"samplesize": "n"})
polls[polls["location"] == "M2"]["margin_poll"]
```

STRONG - one mapping, explained once, units in the names, codes turned into words:

```python
# 538's names -> our names. Everything after this cell uses our names.
POLL_NAMES = {"cycle": "year", "samplesize": "sample_size", "margin_poll": "poll_margin_pts",
              "margin_actual": "result_margin_pts"}
LOCATION_CODES = {"US": "National", "M1": "ME-1", "M2": "ME-2", "N2": "NE-2"}
```

## A checklist

WEAK:

```python
for name, ok in checks.items():
    print(f"{ok!s:>5}  {name}")
```

STRONG:

```python
pd.Series(checks, name="passed")
```
