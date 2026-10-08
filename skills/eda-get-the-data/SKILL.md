---
name: eda-get-the-data
description: Builds the setup notebook that finds, fetches, renames, inspects, and documents the data for an investigation, pulling each piece once and keeping the raw files unchanged. Use after the hypotheses are written and whenever the analysis needs data it does not have.
---

# Get the data

The hypotheses are written (`eda-write-hypotheses`). This stage finds a source that can test them
and produces a dataset whose shape and origin are known. Prose rules are in `eda-write-about-data`,
cell rules in `eda-write-the-notebook`.

## 1. Where the data comes from (setup notebook, section 1)

- Publisher, product, the entity and its identifiers, links to the browse page and the API or file
  documentation.
- Why this source fits the question. Interrogate the data-generating process: who collected it and
  why, what it is composed of, how it was collected and processed before publication, how it is
  distributed and maintained, and which of those is unknown.
- Confirm the data is retrievable before building on it: APIs lag, recent periods may only be in
  bulk files, units differ between products, archives close. Plan a fallback.

*The analyst decides* the source.

## 2. Naming conventions (section 2)

Define the mapping from source names to the notebook's names in one cell, after a markdown cell
that explains the convention. The convention itself is in `eda-write-the-notebook`, Naming.

## 3. The request (section 3)

- Pull the data in code, from the source, so it can be re-run. Keep the raw download unchanged in
  `data/raw/`.
- Use the fetch helper from `eda-run-a-script` for every piece: it returns a piece already on disk that
  passed its check, retries a failed request, checks a response before saving it (not empty; covers
  the requested period and entities), and lists the pieces that failed. Re-request only the failed
  pieces, in a smaller unit if needed. Never start the whole pull over in a different unit.
- Size the request before running it: estimate the number of requests and the time from one test
  request made while planning, and record the estimate in markdown rather than re-running it.
- Pull the smallest set that tests the series A hypotheses as worded: the comparison window they
  name, the variables they need. Say in markdown which window was pulled and why, because ranks
  depend on it. Widen it only when a later hypothesis needs more, and then pull only the addition.
- Rename immediately after loading, then convert units, then derive simple fields (year, day).

## 4. First look (section 4)

Run the inspection routine and show the outputs: `df.shape`, `df.info()`, `df.head()`,
`df.tail()`, `df.sample(5, random_state=0)`, `df.describe()`. Then answer, in markdown, the three
tidy-data sentences:

> This is a dataset about ___. Each row represents ___. The columns represent ___.

State the unit of analysis, the time span and entities covered, and anything surprising.
*The analyst confirms* the unit of analysis.

## 5. Then data quality

Hand over to `eda-check-the-data` (sections 5 and on of the same notebook). When it is done, the
series B hypotheses are written (`eda-write-hypotheses`) before any hypothesis is tested.

## 6. Checks against facts you already know (section 6)

A `pd.Series` of named boolean checks: the right entity, the expected row counts, a value known
from outside the data (a published total, a known event), units in a plausible range, keys
unique. Followed by "**What we found.**"

## 7. Save and provenance (section 7)

Write the cleaned files to `data/` and `data/PROVENANCE.md`: source, request, pull time in UTC
(for a file reused from an earlier pull, the file's saved time, and say so), data version or
commit if available, conversions, fallbacks, decisions that changed rows. Values from recent
periods may be provisional; the pull date matters.

## Reference

- `references/setup-template.md`: the section skeleton of a setup notebook, with the job of each
  section's markdown.
