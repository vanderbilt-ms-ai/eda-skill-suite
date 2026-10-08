---
name: eda-notebook-setup
description: Turns a stakeholder's problem into a brief, questions, and hypotheses, then builds the setup notebook that pulls, checks, and documents the data. Owns the rules for writing hypotheses at every stage. Use at the start of any analysis and whenever a new hypothesis is written.
---

# EDA notebook setup

The analyst receives a problem and nothing else. This stage turns it into questions the data can
answer, hypotheses that can fail, and a dataset whose shape and origin are known. This skill owns
the brief, the hypothesis rules, and the setup notebook's sections. Prose rules are in
`eda-writing-standards`, cell rules in `eda-notebook-standards`.

## 1. The brief (first cell of the analysis notebook)

- Who the analyst is, who is asking, and what situation prompted it.
- The observation, stated before any question (`eda-writing-standards`, Observation before
  question). Write it first as the stakeholder reports it. After the pull, the setup notebook
  computes the observation's numbers in its last section, "The numbers the brief quotes", and the
  brief is updated to cite them. The questions do not change when the numbers arrive.
- The stakeholder's request, quoted.
- The question or questions it reduces to.

*The analyst decides* the questions.

## 2. Hypotheses

Every hypothesis in the investigation, whenever it is written, has the same form:

- One claim, as a full sentence that could be false. A claim that bundles several parts gets split,
  so each has its own verdict.
- "Refuted if": the result that would refute it. A hypothesis with no such result is dropped.
- The smallest difference that would change the stakeholder's decision, not only its direction
  ("refuted if the gain does not recover the extra cost within 10 years", not "refuted if the gain
  is zero or less"). A claim about a rank ("the worst in years") is tested by the rank in a named
  window and needs no margin.
- A number in the order it will be tested, within its question and its series.
- The words of the request it tests, where it tests one: list each word that carries a claim and
  what it requires ("pays off" compares a gain with its cost; "the worst in years" names a window;
  "could we have told in advance" means using only what was known before the outcome).

There are two series, and the difference between them is what the analyst knew when writing.

**Series A: before any data.** Written from the problem statement alone, before the request runs,
and never edited afterwards. They are the explanations already on the table: what the stakeholder
or the people around them say ("the polls had small samples"), the checks the stakeholder would
expect (was it unusual at all?), and one "something else" claim stated at the level of the question
("neither: something about where the polls were taken explains the error"). Two to four per
question is typical. Write them to `hypotheses.md` before the request runs, and insert that file
into the analysis notebook verbatim; `eda-tools/scripts/check_order.py` checks the file predates
the data.

**Series B: after looking.** The first look and the data-quality checks show distributions, gaps,
groups, and ranges that the problem statement could not. Each later finding does the same. A
question those views raise is written as a series B hypothesis, in the same form, before its
section runs, with one more line: what prompted it (the view, the table, or the finding). The first
batch is written in the analysis notebook right after the data-quality section is read, under its
own heading; later ones open the digging-deeper section that tests them. Series B hypotheses are
numbered B1, B2, and so on.

The two series serve different purposes. Series A tests what people already believe, and a failed
series A hypothesis stays failed (`eda-analysis-selection`, The verdict); a better measure that
turns up later is a series B hypothesis, not a repair. Series B is the investigation: it carries the
questions the data itself raised, and it is where most findings come from.

In a student version only, add a prompt for the student's own prediction before any data. An
analyst's deliverable leaves it out.

*The analyst decides* the hypotheses in both series.

## 3. Where the data comes from (setup notebook, section 1)

- Publisher, product, the entity and its identifiers, links to the browse page and the API or file
  documentation.
- Why this source fits the question. Interrogate the data-generating process: who collected it and
  why, what it is composed of, how it was collected and processed before publication, how it is
  distributed and maintained, and which of those is unknown.
- Confirm the data is retrievable before building on it: APIs lag, recent periods may only be in
  bulk files, units differ between products, archives close. Plan a fallback.

*The analyst decides* the source.

## 4. Naming conventions (section 2)

Define the mapping from source names to the notebook's names in one cell, after a markdown cell
that explains the convention. The convention itself is in `eda-notebook-standards`, Naming.

## 5. The request (section 3)

- Pull the data in code, from the source, so it can be re-run. Keep the raw download unchanged in
  `data/raw/`.
- Use the fetch helper from `eda-tools` for every piece: it returns a piece already on disk that
  passed its check, retries a failed request, checks a response before saving it (not empty; covers
  the requested period and entities), and lists the pieces that failed. Re-request only the failed
  pieces, in a smaller unit if needed. Never start the whole pull over in a different unit.
- Size the request before running it: estimate the number of requests and the time from one test
  request made while planning, and record the estimate in markdown rather than re-running it.
- Pull the smallest set that tests the series A hypotheses as worded: the comparison window they
  name, the variables they need. Say in markdown which window was pulled and why, because ranks
  depend on it. Widen it only when a later hypothesis needs more, and then pull only the addition.
- Rename immediately after loading, then convert units, then derive simple fields (year, day).

## 6. First look (section 4)

Run the inspection routine and show the outputs: `df.shape`, `df.info()`, `df.head()`,
`df.tail()`, `df.sample(5, random_state=0)`, `df.describe()`. Then answer, in markdown, the three
tidy-data sentences:

> This is a dataset about ___. Each row represents ___. The columns represent ___.

State the unit of analysis, the time span and entities covered, and anything surprising.
*The analyst confirms* the unit of analysis.

## 7. Then data quality

Hand over to `eda-data-quality` (sections 5 and on of the same notebook). When it is done, the
series B hypotheses are written (section 2 above) before any hypothesis is tested.

## 8. Checks against facts you already know (section 6)

A `pd.Series` of named boolean checks: the right entity, the expected row counts, a value known
from outside the data (a published total, a known event), units in a plausible range, keys
unique. Followed by "**What we found.**"

## 9. Save and provenance (section 7)

Write the cleaned files to `data/` and `data/PROVENANCE.md`: source, request, pull time in UTC
(for a file reused from an earlier pull, the file's saved time, and say so), data version or
commit if available, conversions, fallbacks, decisions that changed rows. Values from recent
periods may be provisional; the pull date matters.

## Reference

- `references/setup-template.md`: the section skeleton of a setup notebook, with the job of each
  section's markdown.
