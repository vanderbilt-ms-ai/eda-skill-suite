---
name: eda-get-data
description: Builds the setup notebook that finds a data source, downloads each piece once, renames the columns, inspects the data, and records where it came from. Use after the first hypotheses are written and whenever the analysis needs more data.
---

# The setup notebook: finding and downloading the data

**Inputs.** `hypotheses.md` (the analyst's brief and first hypotheses, in the form `eda-hypothesis`
sets) and,
if the stakeholder named one, a data source.

**Produces.** `<case>-step0-get-the-data.ipynb` with sections 1 to 4 below, then the sections
`eda-check-data` adds, then sections 6 to 8 below. It writes `data/raw/` (downloads, unchanged),
`data/<clean files>`, and `data/PROVENANCE.md`. The notebook's skeleton is in
`references/setup-template.md`.

Cell rules are in `eda-write-notebook`; prose rules in `eda-write-prose`.

## 1. Where the data comes from

- Name the publisher, the product, the entity each row describes and its identifier, and link the
  browse page and the API or file documentation.
- Say why this source can test the hypotheses.
- Describe how the data was generated: who collected it and why, what it is made of, how it was
  processed before publication, how it is distributed and maintained, and which of those is
  unknown.
- Confirm the data can be retrieved before building on it. APIs lag; recent periods may exist only
  in bulk files; units differ between products; archives close. Name a fallback source.

*The analyst decides* the source.

## 2. Naming conventions

Write a markdown cell explaining the naming convention (`eda-write-notebook`, Naming), then one
code cell with the mapping from the source's column names to the notebook's names.

## 3. The request

- Download in code, from the source, so the notebook can be re-run. Save every download unchanged
  in `data/raw/`.
- Use `fetch.py` from `eda-scripts` for every piece. It returns a piece already on disk that passed
  its check without a request; retries a failed request; checks a response before saving it (not
  empty; the first and last date and the row count match what was asked for); and lists the
  pieces that failed with the reason. Re-run the same call to re-request only the failed pieces,
  in smaller pieces if needed. Do not restart the whole download with different pieces.
- Estimate the number of requests and the time from one test request made while planning. Write
  the estimate in markdown; do not re-run the test request each time the notebook runs.
- Request the smallest set of columns, entities, and years that tests the first hypotheses as
  worded. Say in markdown which years were requested and why, because a rank depends on the years
  compared. Request more only when a later hypothesis needs it, and then request only the
  addition.
- After loading: rename with the mapping, convert units, then derive simple fields (year, day).

## 4. First look

Run and show: `df.shape`, `df.info()`, `df.head()`, `df.tail()`, `df.sample(5, random_state=0)`,
`df.describe()`. Then write, in markdown, the three sentences:

> This is a dataset about ___. Each row represents ___. The columns represent ___.

State the unit of analysis, the time span, the entities covered, and anything surprising.
*The analyst confirms* the unit of analysis.

## 5. Data quality

`eda-check-data` adds its sections here. When they are done, the analyst writes the second set of
hypotheses (form in `eda-hypothesis`) before any hypothesis is tested.

## 6. Checks against facts already known

One `pd.Series` of named boolean checks: the right entity; the expected row counts; a value known
from outside the data (a published total, a known event); units in a plausible range; keys
unique. Followed by a "**What we found.**" cell.

## 7. Save and provenance

Write the clean files to `data/` and write `data/PROVENANCE.md`: source, request, download time in
UTC (for a file reused from an earlier download, the file's saved time, and say so), data version
or commit if the source gives one, unit conversions, fallbacks used, decisions that changed rows.
Say which periods may still be provisional at the source.

## 8. The numbers the brief quotes

Compute the observation's numbers under a "**What was observed.**" label, so the brief can cite
them and the lint can trace them.

## Reference

- `references/setup-template.md`: the section skeleton with the job of each section's markdown
  and three examples from finished cases.
