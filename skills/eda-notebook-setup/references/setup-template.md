# Setup notebook skeleton

Section headings and the job of each section's markdown. Replace the bracketed parts. Every section
that runs a check ends with a "**What we found.**" cell.

```
# Step 0: Getting the Data

**[Course] - [case] case study**

[One paragraph: the request arrived with a question and no data. This notebook finds the source,
pulls the records, puts them in a consistent shape, checks them, and writes down where they came
from. Say if it needs an internet connection.]

By the end you will have, in `data/`:
- `[file].csv` - one row per [unit]: [what the columns hold]
- `PROVENANCE.md` - where it came from, and when

---
## 1. Where the data comes from
[Publisher and product; a table of products, what each holds, and the identifiers used; links to
the browse page and the API/file documentation; why this source fits the question; what is unknown
about how it was collected.]

[code: imports, constants for URLs and paths, a download helper that caches the raw file]

---
## 2. Naming conventions
[Why rename: the source's names only mean something with the documentation open. The rules:
lower_snake_case; the unit in the name; the same name for the same thing in every file; codes
turned into words. Source names appear only in the request.]

[code: the mapping(s)]

---
## 3. The request
[What is requested and why only that; units requested and why; what the raw copy is for.]

[code: request, save raw, rename, convert units, derive simple fields]

---
## 4. First look
[What the inspection routine shows and why it comes before anything else.]

[code: shape, info, head, tail, sample, describe]

[markdown: the three sentences - this is a dataset about ___; each row represents ___; the columns
represent ___ - and the unit of analysis, time span, coverage.]

---
## 5. Data quality
(see eda-data-quality: one subsection per check, each with markdown before, a table or chart, and
"What we found" after - what a row is; missing values; values and units; coverage; preprocessing)

---
## 6. Check against facts you already know
[code: pd.Series of named boolean checks]
**What we found.** [All N checks pass / which fail and what that means.]

---
## 7. Save, and write down where it came from
[code: write cleaned files and PROVENANCE.md; display the provenance text and the saved table's head]
```

## Example opening (from the polls case)

> Two sources cover what we need:
>
> | Source | What it holds | Unit |
> |---|---|---|
> | 538's polls file (GitHub) | the final weeks' polls for six presidential elections, with each race's result | one poll of one race |
> | MIT Election Data and Science Lab (Harvard Dataverse) | official vote counts by state | one candidate in one state and year |
>
> The second source checks the first: 538's result margins against the official counts.

## Example naming section (from the polls case)

> 538 names its columns `cycle`, `location`, `margin_poll`, `samplesize`, and marks places with
> codes like `M2`. We rename everything **once, right after loading**, and use our names everywhere
> after that: lower_snake_case; the unit in the name (`poll_margin_pts`, `dem_pct`); names that say
> what the value is (`result_margin_pts`, not `margin_actual`); codes turned into words (`US`
> becomes `National`, `M2` becomes `ME-2`).
