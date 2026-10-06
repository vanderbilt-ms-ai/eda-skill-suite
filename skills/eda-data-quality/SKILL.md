---
name: eda-data-quality
description: Checks a dataset's quality before analysis, including missing values, and records each decision about what to do with the problems found. Use whenever data has been loaded or cleaning comes up.
---

# Data quality and preprocessing

Every check below runs and is reported, **including when it finds nothing**: "No column has
missing values in the analysis window" is a finding, and the reader needs to see the evidence for
it. A problem nobody checked for quietly produces a wrong number later. A check that cannot apply
to this data gets one line, "**Does not apply:** [why]", instead of a section.

This stage looks at one variable at a time and at how the data was recorded. It does not plot the
outcome against the variables the hypotheses name; that is the analysis, and it comes after the
hypotheses are fixed (`eda-workflow`).

Each check is one subsection of the setup notebook's data-quality section, with three parts:
markdown before (what is checked and why it matters for this question), a labelled table or chart,
and "**What we found.**" (the result with its number, and what it means for the analysis). Where a
problem needs a choice, add an "**Analyst decision.**" paragraph (see `eda-workflow`). Code
snippets for each check are in `references/checks.md`.

## 1. What a row is

- Confirm the unit of analysis from `eda-notebook-setup` holds for every row.
- **Duplicates**: fully duplicated rows; duplicated keys (the same entity and time twice).
- **Aggregate rows** mixed in with ordinary rows (totals, "All", national rows among states).
- **Several units in one table** (readings and summaries; routine and special reports).
- **Values copied across entities**: identical values within a group that should vary (branch
  campuses repeating their parent's earnings). Check `groupby(key)[col].nunique()`.
- **Irregular time series**: the number of rows per period differs, so counting rows does not count
  hours or days. List the kinds of rows (routine readings, special or corrected reports, summaries)
  and how many of each fall in each period. Choose which reading represents each period (the
  routine reading, the last one, the mean of all) and say why; averaging every report type together
  is a choice too. **Check that the choice does not drop data**: one period's values can be split
  across two reports, and a special report can hold events (a weather code, a correction) that the
  routine report lacks. If choosing one report loses values, combine column by column (the value
  from whichever report has it) and say which columns came from where. Then resample to one value
  per period before counting.
- **The record's format over time**: a source's columns, codes, or report types can change between
  years. Check that each column means the same thing in every year pulled.

## 2. Missing values (always run, always report)

1. **Count and share** missing per column, overall. Treat sentinel codes as missing first:
   `"PrivacySuppressed"`, `"PS"`, `"NULL"`, `"NA"`, `""`, whitespace, `-999`, `9999`, impossible
   zeros. Do not rely on a fixed list: find every text value in a column that should be numeric
   (`references/checks.md`), because each release can use its own codes.
2. **By group**: missing share per column by year, entity type, or other grouping the questions use.
   Missingness concentrated in one period or one kind of entity changes what a comparison means.
3. **Blank vs zero vs not recorded**: is a blank "zero" (nothing happened), "not recorded" (a
   flag nobody sets), "not applicable" (a question not asked of this respondent), or
   "unknown"? Read the documentation; check it against cases where the answer is known.
4. **Missing by design**: split-sample survey questions, fields that only exist for some entity
   types, periods before a field existed. **The meaning of a blank can change within one column**
   (blank meant "not recorded" in early years and "zero" in later ones): check what a blank means
   in each year, against cases where the answer is known.
5. **Is it random?** Compare rows where the value is missing with rows where it is present, on the
   other variables (`references/checks.md` has the snippet). If they differ, the values are not
   missing completely at random, and any analysis restricted to complete rows describes a different
   population. Name who created the gap: the subject (refused, did not report) or the collector
   (not asked, not measured, suppressed for privacy).
6. **Gaps in a series**: list every missing period inside the windows the questions use, with the
   values on either side. Any measure that depends on continuity (the longest run past a threshold,
   a duration, a cumulative count) is cut short by a gap unless it is handled. Compute such a
   measure both ways - the gap breaks the run; the gap is filled when the values on both sides are
   past the threshold - report both, and say which one the findings use and why. Never let a gap
   silently shorten a run.
7. **What each analysis will do with it**: a regression or `dropna` drops incomplete rows
   silently; `mean` skips blanks; a sum treats them as zero only if filled. State how many rows each
   planned analysis will actually use.
8. **Decision** (*the analyst decides*): drop the rows, keep them and narrow the question's scope,
   impute (only with a stated method and a flag column marking imputed values), or get the data
   another way. Write the reason.

## 3. Values and units

- **Units** consistent across sources, products, and years (one source in Fahrenheit, another in
  Celsius; percent vs proportion). Check that every group's values sit in the same range.
- **Ranges**: impossible values (negative counts, shares above 1, temperatures of 999).
- **Outliers**: flag by a quantile or z-score rule; for each, argue keep or drop from what it is,
  never drop by rule alone. Show the distribution (histogram or box plot).
- **Categories**: inconsistent labels (whitespace, case, synonyms, codes); collapse rare
  categories only with a reason.
- **Dates and times**: parsed on import; one time zone; the window the question needs.
- **Money from different years**: dollars measured in different years (earnings in 2022 dollars,
  prices in 2024 dollars) are not comparable until converted to one year's dollars with a price
  index (the Consumer Price Index). Say which index and which year.
- **Two columns for one concept** (academic-year cost vs program-year cost): combine with a rule
  and say which rows used which.
- **Which period each column describes**: in a table of summaries, columns can describe different
  years (this year's price beside the earnings of people who started ten years ago). Make a table of
  each column the analysis uses and the period it describes, from the documentation, and say what a
  mismatch means for the questions.

## 4. Coverage, the pull itself, and a second source

- **Every response covers what was requested**: for each piece downloaded, the first and last date
  (or the entities) and the row count against what was requested. An API can return "success" with
  an empty or cut-off file. A table: piece requested, rows, first date, last date, complete or not.

- What the data covers and what it does not (years, entities, kinds of cases); what that leaves out
  of the question's scope.
- Where a second source exists, check a sample of values against it (the results file against
  official counts) and report the largest difference.

## 5. Preprocessing

Only what the questions need, each step explained before it runs:
- **the unit each comparison counts**: each entity once (every college counts the same) or weighted
  by size (each student counts the same). They answer different questions; *the analyst decides*
  which the question asks, and says so;
- reshape (long or wide) to the shape the analysis needs, and say why;
- derived variables (feature engineering): define them, and say what they assume;
- transformations (log for a skewed range, scaling for distance-based methods, encoding for
  categories) when a planned method requires them - `eda-lens` says which;
- save the cleaned table; the raw download stays unchanged.

## Reference

- `references/checks.md` - pandas snippets for every check, written to the notebook standards
  (labelled tables, no print statements).
