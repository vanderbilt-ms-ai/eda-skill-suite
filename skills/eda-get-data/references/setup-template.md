# Setup notebook skeleton

Section headings and the job of each section's markdown. Replace the bracketed parts. Every section
that runs a check ends with a "**What we found.**" cell. The opening cell states what the notebook
holds; it does not narrate what the notebook is about to do (`eda-write-prose`, No framing
sentences).

```
# Step 0: Getting the Data

**[Course or team] - [case]**

[The request, in one sentence, and the question it reduces to. Whether the notebook needs an
internet connection.]

Files written to `data/`:
- `[file].csv`: one row per [unit]; [what the columns hold]
- `PROVENANCE.md`: source, request, pull time

---
## 1. Where the data comes from
[Publisher and product; a table of products, what each holds, and the identifiers used; links to
the browse page and the API or file documentation; why this source fits the question; what is
unknown about how it was collected.]

[code: imports, constants for URLs and paths, `from tools.fetch import fetch`]

---
## 2. Naming conventions
[The convention in two or three sentences; see eda-write-notebook, Naming.]

[code: the mapping(s)]

---
## 3. The request
[What is requested and why only that; units requested and why; the size estimate from the test
request.]

[code: fetch each piece, save raw, rename, convert units, derive simple fields; the fetch
helper's table of pieces, rows, first and last date, status]

---
## 4. First look
[code: shape, info, head, tail, sample, describe]

[markdown: the three sentences; the unit of analysis, time span, coverage]

---
## 5. Data quality
(eda-check-data: one subsection per check or group of checks, each with markdown before, a table
or chart, and "What we found" after)

---
## 6. Check against facts you already know
[code: pd.Series of named boolean checks]
**What we found.** [All N checks pass, or which fail and what that means.]

---
## 7. Save, and write down where it came from
[code: write cleaned files and PROVENANCE.md; display the provenance text and the saved table's
head]

---
## 8. The numbers the brief quotes
[code: the observation's numbers, under a "What was observed." label in the output's markdown]
```

## Example opening of section 1 (2020 polls case)

> Two sources cover what we need:
>
> | Source | What it holds | Unit |
> |---|---|---|
> | 538's polls file (GitHub) | the final weeks' polls for six presidential elections, with each race's result | one poll of one race |
> | MIT Election Data and Science Lab (Harvard Dataverse) | official vote counts by state | one candidate in one state and year |
>
> The second source checks the first: 538's result margins against the official counts.

## Example naming section (2020 polls case)

> 538 names its columns `cycle`, `location`, `margin_poll`, `samplesize`, and marks places with
> codes like `M2`. We rename everything once, right after loading, and use our names everywhere
> after that: lower_snake_case; the unit in the name (`poll_margin_pts`, `dem_pct`); names that say
> what the value is (`result_margin_pts`, not `margin_actual`); codes turned into words (`US`
> becomes `National`, `M2` becomes `ME-2`).

## Example series B hypotheses (Nashville ice storm case)

Written after the first look and the data-quality checks, which showed that the hourly record
carries a precipitation type and that January 2026 was ordinary on the monthly measures:

> **B1. The storm's freezing rain, not its total precipitation, set it apart.** Prompted by the
> first look: the hourly file reports precipitation type, and the monthly totals (section 5.3)
> were ordinary. *Refuted if* at least three earlier winters had a freezing-rain episode with as
> much liquid.
>
> **B2. The cold after the storm lasted longer than after any earlier freezing-rain episode.**
> Prompted by the gap check (section 5.5), which showed the hourly temperature series is complete
> enough to count hours. *Refuted if* any earlier episode was followed by as many hours at or below
> 32 F in the next 168.
