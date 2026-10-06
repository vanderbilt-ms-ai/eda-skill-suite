---
name: eda-notebook-setup
description: Turn a stakeholder's problem into the start of an EDA - the brief (role, stakeholder, the observation with its numbers, the questions), falsifiable hypotheses, and a setup notebook that finds the data source, pulls the data itself, renames columns to consistent conventions, runs the first-look inspection (info, head, tail, sample, describe, the three tidy-data sentences, the unit of analysis), checks the data against facts already known, and records provenance. Use this skill at the start of any analysis, whenever someone hands over a problem, an email, or a dataset, even if they only say "here is the data" or "can you get the numbers on X".
---

# EDA notebook setup

The analyst receives a problem and nothing else. This stage turns it into a question the data can
answer and a dataset whose shape and origin are known. Follow `notebook-standards`,
`figure-standards`, and `writing-standards` in every cell.

## 1. The brief (first cell of the analysis notebook)

- Who the analyst is, who is asking, and what situation prompted it, in plain sentences.
- **The observation, stated specifically before any question**: what was measured, by how much,
  compared with what ("National polls put Biden ahead by 8.4 points on average; he won by 4.4").
  If the numbers come from the data, compute them in the setup notebook and fill them in.
- The stakeholder's request, quoted.
- The question or questions it reduces to, worded to match the observation and no broader
  ("Why were the polls off?", not "What went wrong?").
- If the observation's numbers come from the data, the setup notebook computes them in a short
  final section, "The numbers the brief quotes", and the brief cites it.

*The analyst decides* the questions.

## 2. Hypotheses, written before any data is pulled

The hypotheses and what would refute each one are written **before the request runs**, from the
problem statement alone, and they do not change after the data arrives. Create the analysis
notebook at this point with only its brief and its "Hypotheses" section (the setup cell comes
between them later). If a later look at the data suggests a better hypothesis or threshold, it
becomes a **new question** in its own section, labelled as such; the original stands with its own
verdict.

**Which hypotheses come first.** The opening hypotheses are the explanations already on the table,
not the analyst's own theory of what happened:
- the explanations the stakeholder, or the people around them, already give ("it was the coldest,
  wettest January in years"; "the polls had small samples") - tested exactly as worded, because they
  are usually wrong and testing them is the point;
- the obvious checks the stakeholder would expect (was it unusual at all?);
- **one** "something else" hypothesis, stated at the level of the question, not as a mechanism:
  "Neither: something about the storm itself, not the month as a whole, made it different." It is
  one claim, with one verdict.

Do **not** write opening hypotheses that need knowledge of what the data will show: a specific
mechanism, a measure you would only think of after looking, a threshold chosen from the case. Those
arrive later as digging-deeper questions, each one prompted by a finding, and that sequence is the
investigation. Two to four hypotheses per question is typical; seven is a sign the analyst has
written the answer in advance.

- Each question gets its own numbered hypotheses, as full sentences that could be false.
- **Test the stakeholder's words.** List the words in the request that carry a claim and say what
  each one requires: "pays off" compares a gain with its cost, not only "more goes with more";
  "coldest in years" names a window (say which, and pull it); "could we have told in advance"
  means using only what was known before the outcome.
- **Say how big a difference has to be to matter.** Each refutation names the smallest difference
  that would change the stakeholder's decision, not only its direction ("refuted if the gain does
  not recover the extra cost within 10 years", not "refuted if the gain is zero or less"). A
  difference in the right direction but below that size does not make the hypothesis hold.
- **One claim per hypothesis.** A hypothesis that bundles several claims ("the month was cold and
  wet and windy") gets split, so each has its own verdict. "Holds on one of three parts" is not a
  verdict.
- **Claims about a rank** ("the coldest in years"): the rank in the named window is the test; a
  margin is not needed. If one is wanted, base it on the ordinary year-to-year spread (the standard
  deviation across years), not on a number invented for the case.
- Number the hypotheses in the order they will be tested.
- For each, write down the result that would refute it. Drop any hypothesis with no such result.
- In a student version only: a prompt for the student's own prediction before any data ("My
  prediction, before looking at any data: ... and why"). An analyst's deliverable leaves it out.

*The analyst decides* the hypotheses.

## 3. Where the data comes from (setup notebook, section 1)

- Publisher, product, the entity and its identifiers (station, institution, poll), links to the
  browse page and the API or file documentation.
- Why this source fits the question. Interrogate the data-generating process: who collected it and
  why, what it is composed of, how it was collected and processed before publication, how it is
  distributed and maintained, and which of those is unknown.
- Confirm the data is actually retrievable before building on it: APIs lag, recent periods may only
  be in bulk files, units differ between products, archives close. Plan a fallback.

*The analyst decides* the source.

## 4. Naming conventions (section 2)

Explain the convention in markdown, then define the mapping(s) in one cell: source names to
lower_snake_case names with units (`margin_poll` to `poll_margin_pts`), codes to words. Everything after this cell
uses the new names. Source names appear only in the request.

## 5. The request (section 3)

- Pull the data in code, from the source, so it can be re-run. Keep the raw download unchanged in
  `data/raw/`.
- **Download each piece once.** The download helper must:
  1. return the file in `data/raw/` without a request when it is already there and has passed the
     check below;
  2. otherwise request it, retrying a slow or failed request a few times;
  3. **check the response before saving it**: not empty, and it covers the requested period and
     entities (first and last date, row count against the expected count). An API can answer
     "success" with an empty or cut-off file;
  4. save only a response that passes, and list the pieces that failed.
  Then re-request **only the failed pieces**, in a smaller unit if needed (one month instead of a
  winter). Never re-download pieces that already passed, and never start the whole pull over in a
  different unit.
- **Size the request before running it.** Estimate the number of requests and the time from one
  test request, made once while planning; record the estimate in markdown rather than re-running
  the test request every time the notebook runs. Pull the smallest set that tests the hypotheses as worded (the comparison window the
  hypotheses name, the variables they need). Widen it only when a later question needs more, and
  then pull only the addition. Say in markdown which window was pulled and why, because ranks and
  "the most in N years" depend on it.
- Ask for only what the questions need (columns, period, entities), and say why in markdown.
- Rename immediately after loading, then convert units, then derive simple fields (year, day).

## 6. First look (section 4)

Run the inspection routine and show the outputs (they are the evidence for what follows):
`df.shape`, `df.info()`, `df.head()`, `df.tail()`, `df.sample(5, random_state=0)`, `df.describe()`.
Then answer, in markdown, the three tidy-data sentences:

> This is a dataset about ___. Each row represents ___. The columns represent ___.

State the **unit of analysis**, the time span and entities covered, and anything surprising.
*The analyst confirms* the unit of analysis.

## 7. Then data quality

Hand over to `eda-data-quality` (sections 5 and on of the same notebook). Every check runs and is
reported, even when the data is clean.

## 8. Checks against facts you already know

A `pd.Series` of named boolean checks: the right entity, the expected row counts, a value you know
from outside the data (a published total, a known event), units in a plausible range, keys unique.
Followed by "**What we found.**"

## 9. Save and provenance

Write the cleaned files to `data/` and a `data/PROVENANCE.md`: source, request, pull time (UTC; for
a file reused from an earlier pull, the file's saved time, and say so),
data version or commit if available, conversions, fallbacks, decisions that changed rows. Values
from recent periods may be provisional; the pull date matters.

## Reference

- `references/setup-template.md` - the section skeleton of a setup notebook, with the markdown each
  section needs, taken from finished case studies.
