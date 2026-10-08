---
name: eda-check-data
description: Runs the data-quality checks on a loaded dataset, missing values included, and records each decision about what to do with the problems found. Use whenever data has been loaded or cleaning comes up.
---

# The data-quality checks

**Inputs.** The setup notebook after its first look (`eda-get-data`, section 4): the renamed data
in memory, and the fetch table of pieces downloaded.

**Produces.** The data-quality section of the setup notebook (section 5), one subsection per
check or group of related checks, and the preprocessing that follows it. Each subsection has the
three parts every section has (`eda-write-notebook`, Structure). A problem that needs a choice
gets an "**Analyst decision.**" paragraph (`eda-investigate`, Handing decisions back). Code for
each check is in `references/checks.md`.

Every check runs and is reported, including a check that finds nothing: "No column has missing
values in the years compared" is a finding, and the reader needs the evidence. A check that
cannot apply to this data gets one line, "**Does not apply:** [why]". Related checks that find
nothing share one table. The whole section runs about 20 to 30 cells.

Each check examines one variable, or how the data was recorded. A comparison that tests a
hypothesis belongs in the analysis notebook. What these views suggest is written down
afterwards as the second set of hypotheses (`eda-write-hypotheses`).

## 1. What a row is

- Confirm that the unit of analysis stated in the first look holds for every row.
- Duplicates: rows duplicated in full; keys duplicated (the same entity at the same time twice).
- Summary rows mixed with ordinary rows: totals, "All", a national row among states.
- Several kinds of row in one table: readings and summaries; routine reports and special reports.
- Values copied across entities: identical values within a group that should vary; check
  `groupby(key)[col].nunique()`. Example: branch campuses that repeat their parent's earnings.
- Irregular time series: the number of rows per hour or day varies, so counting rows does not
  count hours or days. List the kinds of row and how many of each fall in each period. Choose
  which row represents each period and say why. Check that the choice loses nothing: one period's
  values can be split across two rows, and a rarer kind of row can hold events the routine kind
  lacks. If so, combine column by column and say which column came from which kind of row. Then
  resample to one value per period before counting. Example: airport weather files with routine
  hourly reports and special reports in the same file.
- Changes in the record over time: columns, codes, and report types can change between years.
  Check that each column means the same thing in every year requested.

## 2. Missing values

1. Count and share missing per column. First turn sentinel codes into missing values. Do not rely
   on a fixed list: list every text value in a column that should be numeric, and every numeric
   value that is a code (-999, 9999, an impossible zero), because each release can use its own
   codes. Codes seen so far: "PrivacySuppressed", "PS", "NULL", blank, whitespace.
2. By group: the share missing per column by year, entity type, or any grouping the questions use.
   Missingness concentrated in one period or one kind of entity changes what a comparison means.
3. Blank, zero, or not recorded: decide whether a blank means zero, not recorded, not applicable,
   or unknown. Read the documentation, and check it against cases where the answer is known.
4. Missing by design: questions asked of only part of a sample, fields that exist only for some
   entity types, periods before a field existed. The meaning of a blank can change within one
   column across years; check it in each year against cases where the answer is known.
5. Random or not: compare the rows where the value is missing with the rows where it is present,
   on the other variables. If they differ, the values are not missing at random, and an analysis
   of complete rows describes a different population. Name who created the gap: the subject
   (refused, did not report) or the collector (not asked, not measured, suppressed).
6. Gaps in a series: list every missing period inside the years the questions use, with the values
   on either side. A measure that depends on continuity (the longest run past a threshold, a
   duration, a cumulative count) is cut short by a gap unless the gap is handled. Compute such a
   measure both ways: the gap breaks the run; the gap is filled when the values on both sides are
   past the threshold. Report both, and say which one the findings use. This is the only place
   this rule is written; `eda-test-hypothesis` and `eda-verify` refer to it.
7. What each planned analysis will do with missing values: a regression or `dropna` drops
   incomplete rows silently; `mean` skips blanks; a sum counts them as zero only if filled. State
   how many rows each planned analysis will use.
8. Decision (*the analyst decides*): drop the rows; keep them and narrow the question; impute,
   only with a stated method and a flag column marking imputed values; or get the data another
   way. Write the reason.

## 3. Values and units

- Units: the same across sources, products, and years. Check that every group's values sit in the
  same range. Examples: one source in Fahrenheit and another in Celsius; percent against
  proportion.
- Ranges: impossible values (negative counts, shares above 1, a temperature of 999).
- Outliers: flag by a quantile or z-score rule; for each, argue keep or drop from what it is. Do
  not drop by rule alone. Show the distribution.
- Categories: inconsistent labels (whitespace, case, synonyms, codes). Collapse rare categories
  only with a reason.
- Dates and times: parsed on import; one time zone; the period the question needs.
- Money from different years: convert to one year's dollars with a price index before comparing.
  Say which index and which year.
- Two columns for one concept: combine with a rule and say which rows used which. Example:
  academic-year cost against program-year cost.
- The period each column describes: in a table of summaries, columns can describe different
  years (this year's price beside the earnings of people who enrolled ten years ago). Make a table
  of each column the analysis uses and the period it describes, and say what a mismatch means
  for the questions.

## 4. Coverage and a second source

- Show the fetch table (`eda-scripts`, `fetch.py`): piece, status, rows, first date, last date,
  reason. Read it: every piece covers what was requested.
- State what the data covers and what it does not (years, entities, kinds of cases), and what
  that leaves outside the question.
- Where a second source exists, check a sample of values against it and report the largest
  difference. Example: a polls file's reported results against official vote counts.

## 5. Preprocessing

Only what the hypotheses need, each step explained before it runs:
- the unit each comparison counts: each entity once, or each entity weighted by its size. The two
  answer different questions; *the analyst decides* which the question asks, and says so;
- reshape to the shape the analysis needs, and say why;
- derived variables: define each and say what it assumes;
- transformations a planned method requires (log for a skewed range, scaling for distance-based
  methods, encoding for categories); `eda-model` says which;
- save the clean table. The raw download stays unchanged.

## Reference

- `references/checks.md`: pandas code for every check, written to the notebook rules.
