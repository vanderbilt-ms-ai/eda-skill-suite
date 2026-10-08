---
name: eda-check-the-data
description: Checks a dataset's quality before analysis, including missing values, and records each decision about what to do with the problems found. Use whenever data has been loaded or cleaning comes up.
---

# Data quality and preprocessing

Every check below runs and is reported, including when it finds nothing: "No column has missing
values in the analysis window" is a finding, and the reader needs the evidence for it. A problem
nobody checked for quietly produces a wrong number later.

This stage looks at one variable at a time and at how the data was recorded. A comparison that
tests a hypothesis belongs in the analysis notebook (`eda-test-a-hypothesis`). What these views
suggest is not lost: when the section is done, the analyst writes series B hypotheses from it
(`eda-write-hypotheses`, Hypotheses).

Each check, or group of related checks, is one subsection with the three parts every section has
(`eda-write-the-notebook`, Structure). Where a problem needs a choice, add an "**Analyst
decision.**" paragraph (`eda-investigate`, Handing decisions back). Code for each check is in
`references/checks.md`.

**Budget.** A check that finds nothing is one row of a shared table and one line in "What we
found"; a check that cannot apply is one line, "**Does not apply:** [why]". Several related checks
share one table. The whole data-quality section runs about 20 to 30 cells; a problem that needs
its own subsection earns one.

## 1. What a row is

- Confirm the unit of analysis from the first look holds for every row.
- Duplicates: fully duplicated rows; duplicated keys (the same entity and time twice).
- Aggregate rows mixed with ordinary rows (totals, "All", a national row among states).
- Several units in one table (readings and summaries; routine and special reports).
- Values copied across entities: identical values within a group that should vary. Check
  `groupby(key)[col].nunique()`. Example: branch campuses that repeat the parent institution's
  earnings.
- Irregular time series: the number of rows per period differs, so counting rows does not count
  periods. List the kinds of rows and how many of each fall in each period. Choose which row
  represents each period and say why. Check that the choice drops nothing: one period's values can
  be split across rows, and a rarer kind of row can hold events the routine kind lacks. If it
  does, combine column by column and say which columns came from where. Then resample to one
  value per period before counting. Example: airport weather with routine hourly reports and
  special reports in the same file.
- The record's format over time: a source's columns, codes, or report types can change between
  years. Check that each column means the same thing in every period pulled.

## 2. Missing values (always run, always report)

1. Count and share missing per column. Treat sentinel codes as missing first. Do not rely on a
   fixed list: find every text value in a column that should be numeric (`references/checks.md`),
   and every numeric value that is a code (-999, 9999, an impossible zero), because each release
   can use its own codes. Examples seen: "PrivacySuppressed", "PS", "NULL", blank, whitespace.
2. By group: missing share per column by period, entity type, or any grouping the questions use.
   Missingness concentrated in one period or one kind of entity changes what a comparison means.
3. Blank vs zero vs not recorded: is a blank "zero", "not recorded", "not applicable", or
   "unknown"? Read the documentation; check it against cases where the answer is known.
4. Missing by design: split-sample questions, fields that exist only for some entity types,
   periods before a field existed. The meaning of a blank can change within one column over time;
   check what a blank means in each period against cases where the answer is known.
5. Is it random? Compare rows where the value is missing with rows where it is present, on the
   other variables. If they differ, the values are not missing completely at random, and an
   analysis of complete rows describes a different population. Name who created the gap: the
   subject (refused, did not report) or the collector (not asked, not measured, suppressed).
6. Gaps in a series: list every missing period inside the windows the questions use, with the
   values on either side. Any measure that depends on continuity (the longest run past a
   threshold, a duration, a cumulative count) is cut short by a gap unless it is handled. Compute
   such a measure both ways (the gap breaks the run; the gap is filled when the values on both sides
   are past the threshold), report both, and say which one the findings use. This is the owner of
   that rule; the analysis and verify skills refer to it.
7. What each analysis will do with it: a regression or `dropna` drops incomplete rows silently;
   `mean` skips blanks; a sum treats them as zero only if filled. State how many rows each planned
   analysis will use.
8. Decision (*the analyst decides*): drop the rows, keep them and narrow the question's scope,
   impute (only with a stated method and a flag column marking imputed values), or get the data
   another way. Write the reason.

## 3. Values and units

- Units consistent across sources, products, and periods. Check that every group's values sit in
  the same range. Examples: one source in Fahrenheit and another in Celsius; percent vs
  proportion.
- Ranges: impossible values (negative counts, shares above 1, a temperature of 999).
- Outliers: flag by a quantile or z-score rule; for each, argue keep or drop from what it is, never
  drop by rule alone. Show the distribution.
- Categories: inconsistent labels (whitespace, case, synonyms, codes); collapse rare categories
  only with a reason.
- Dates and times: parsed on import; one time zone; the window the question needs.
- Values measured in different years' money: not comparable until converted to one year's dollars
  with a price index. Say which index and which year.
- Two columns for one concept: combine with a rule and say which rows used which. Example:
  academic-year cost vs program-year cost.
- Which period each column describes: in a table of summaries, columns can describe different
  periods (this year's price beside the earnings of people who started ten years ago). Make a
  table of each column the analysis uses and the period it describes, and say what a mismatch
  means for the questions.

## 4. Coverage, the pull itself, and a second source

- Every response covers what was requested: the fetch helper's table (`eda-run-a-script`) of piece, rows,
  first and last date or entity, and status is shown here and read.
- What the data covers and what it does not (periods, entities, kinds of cases); what that leaves
  out of the question's scope.
- Where a second source exists, check a sample of values against it and report the largest
  difference. Example: a polls file's reported results against official vote counts.

## 5. Preprocessing

Only what the questions need, each step explained before it runs:
- the unit each comparison counts: each entity once or weighted by size. They answer different
  questions; *the analyst decides* which the question asks, and says so;
- reshape (long or wide) to the shape the analysis needs, and say why;
- derived variables: define them, and say what they assume;
- transformations (log for a skewed range, scaling for distance-based methods, encoding for
  categories) when a planned method requires them; `eda-apply-a-lens` says which;
- save the cleaned table; the raw download stays unchanged.

## Reference

- `references/checks.md`: pandas snippets for every check, written to the notebook standards.
