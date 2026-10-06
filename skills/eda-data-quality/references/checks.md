# Check snippets

Each snippet ends in a displayed table or chart (no print statements). Adapt names to the dataset's
renamed columns.

## Sentinels to missing

```python
SENTINELS = ["PrivacySuppressed", "NULL", "NA", "", " "]
raw = raw.replace(SENTINELS, np.nan)
(raw == -999).sum()[lambda s: s > 0]          # numeric sentinels: check before replacing
```

## Missing values per column

```python
missing = pd.DataFrame({"missing": df.isna().sum(), "share missing": df.isna().mean().round(3)})
missing.sort_values("share missing", ascending=False)
```

## Missing by group

```python
df.drop(columns=["year"]).isna().groupby(df["year"]).mean().round(3)
```

A heatmap helps when there are many columns and groups:

```python
share = df.drop(columns=["year"]).isna().groupby(df["year"]).mean()
fig, ax = plt.subplots(figsize=(9, 4))
image = ax.imshow(share.T, aspect="auto", cmap="Greys", vmin=0, vmax=1)
ax.set_xticks(range(len(share.index)), share.index)
ax.set_yticks(range(len(share.columns)), share.columns)
ax.set(title="Share of values missing, by column and year", xlabel="Year", ylabel="Column")
fig.colorbar(image, label="Share missing (0 to 1)")
```

## Blank vs zero

```python
pd.DataFrame({"blank": df["amount"].isna().sum(),
              "zero": (df["amount"] == 0).sum(),
              "above zero": (df["amount"] > 0).sum()}, index=["rows"])
```

## Is the missingness random? Compare rows with and without the value

```python
has_sat = df["sat_avg"].notna().map({True: "SAT reported", False: "SAT missing"})
df.groupby(has_sat)[["earnings_usd", "admit_rate", "cost_usd"]].median().round(2)
```

Also by category:

```python
pd.crosstab(df["control"], df["sat_avg"].isna(), normalize="index").round(2) \
  .rename(columns={False: "reported", True: "missing"})
```

If the groups differ, the value is not missing at random: an analysis of complete rows describes
only the reporting group.

## Rows each analysis will actually use

```python
needed = ["earnings_usd", "sat_avg", "cost_usd"]
pd.Series({"all rows": len(df), "complete for the regression": len(df.dropna(subset=needed))})
```

## Hourly gaps in an irregular series

```python
per_hour = (hourly.set_index("time").groupby("year")["temp_f"].resample("1h").mean())
gaps = per_hour.isna().groupby(level="year").sum().rename("hours with no reading")
pd.DataFrame({"readings": hourly.groupby("year").size(), "hours with no reading": gaps})
```

## Duplicates and copied values

```python
pd.Series({"duplicate rows": df.duplicated().sum(),
           "duplicate keys": df.duplicated(["unit_id", "year"]).sum()})

shared = df.dropna(subset=["earnings_usd"]).groupby("parent_id")
copies = shared["earnings_usd"].nunique()[shared.size() > 1]
pd.Series({"groups with several rows": len(copies),
           "groups where every row has the same value": (copies == 1).sum()})
```

## Units consistent across groups

```python
df.groupby(["year", "source"])["temp_f"].describe()[["min", "mean", "max"]].round(1)
```

## Outliers by quantile rule

```python
low, high = df["value"].quantile([0.01, 0.99])
df[(df["value"] < low) | (df["value"] > high)].sort_values("value")
```

## Second-source check

```python
check = ours.join(official, how="inner")
check["difference"] = check["ours"] - check["official"]
check.reindex(check["difference"].abs().sort_values().index).tail(5).round(2)
```
