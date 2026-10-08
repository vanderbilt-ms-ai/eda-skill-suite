---
name: eda-write-hypotheses
description: Writes the brief and the hypotheses of an investigation, first from the request alone and later from what the data shows, each with the result that would refute it. Use at the start of an analysis and whenever a finding raises a question.
---

# The brief and the hypotheses

**Inputs.** At the start: the stakeholder's request as it arrived, and nothing else. Later: the
outputs of the setup notebook (the first look and the data-quality checks) or a finding in the
analysis notebook.

**Produces.** At the start: `hypotheses.md` in the project folder, holding the brief and the first
hypotheses; the same text becomes the first two cells of the analysis notebook. Later: a
hypothesis written into the analysis notebook at the point it is needed.

The two notebooks are defined in `eda-investigate`.

## The brief

The brief is the first cell of the analysis notebook. It is written from the request. It holds:
- who the analyst is, who is asking, and what happened that made them ask;
- the observation, stated before any question: what was measured, by how much, compared with what
  (`eda-write-prose`, Observation before question). At this point the numbers are the
  stakeholder's. After the data is downloaded, the setup notebook computes them in its last
  section and the brief is updated to cite them. The questions do not change when the numbers
  arrive;
- the stakeholder's request, quoted;
- the question or questions the request reduces to.

*The analyst decides* the questions.

## What every hypothesis contains

- One claim, as a full sentence that could be false. A claim with several parts ("the month was
  cold and wet and windy") is split into one hypothesis per part.
- At most 80 words in total, claim and refutation included. A longer hypothesis holds two claims
  or an argument for the claim; the argument goes in the section that tests it. The lint reports
  a longer one.
- "Refuted if", followed by the result that would refute it. A claim with no such result is not a
  hypothesis and is dropped.
- The smallest difference that would change the stakeholder's decision, not only the direction
  of the difference. "Refuted if the gain does not recover the extra cost within 10 years", not
  "refuted if the gain is zero or less". A claim about a rank ("the worst in years") is tested by
  the rank within a named span of years and needs no margin.
- A number, in the order the hypotheses will be tested, within the question they belong to.
- Where the hypothesis tests a word of the request, the word and what it requires. "Pays off"
  requires a gain compared with its cost. "The worst in years" requires a span of years, named.
  "Could we have told in advance" requires using only what was known before the outcome.

## The first set: from the request alone

Written before the request for data is sent, from the problem statement alone, and never edited
afterwards. The first set holds:
- the explanations the stakeholder and the people around them already give ("the polls had small
  samples");
- the checks the stakeholder would expect ("was the month unusual at all?");
- one hypothesis that says something else explains it, stated at the level of the question and
  not as a mechanism ("neither: something about where the polls were taken explains the error").

Two to four per question is usual. Seven means the analyst has written the answer in advance.

The first set does not hold the analyst's own theories of mechanism. "The link is a genre
artifact", "there is a ceiling effect past a point", and "the pattern is drift over the years"
are explanations an analyst thinks of, not explanations the stakeholder gave, and each needs a
look at the data to be worth testing. They belong to the second set, written after the first
look, with the view that prompted them named. The split shows the reader which beliefs came
before the data and which the data suggested.

When the stakeholder's word names something the data cannot measure ("streams", when the
available data holds a popularity score), say so in the hypothesis and in `decisions.md`, and
test the closest measure under its own name.

Write them to `hypotheses.md`, then run `check_order.py --stamp` (`eda-scripts`) before any data
is downloaded. The analysis notebook's hypotheses cell is this file, inserted verbatim. A failed
hypothesis from the first set stays failed; it is not re-tested with a different measure
(`eda-test-hypothesis`, The verdict).

## The second set: from what the data shows

The first look and the data-quality checks show distributions, gaps, groups, and ranges the
request did not mention. Each later finding shows more. A question raised by one of those views is
written as a hypothesis in the form above, plus one line: what prompted it (the table, the chart,
or the finding, by section number).

The first batch is written in the analysis notebook right after the data-quality section has been
read, under the heading "## Second hypotheses (from the data)", before any hypothesis is tested.
The lint reports an analysis notebook that has the first set and not this heading. The batch
holds at least two hypotheses; the first look and the quality checks show more than one thing the
request did not mention. Later ones open the section that
tests them. They are numbered B1, B2, and so on, so the reader can tell which hypotheses were
written before the data and which after.

Example, from the Nashville ice storm case. The first look showed that the hourly file records the
type of precipitation, and the quality checks showed January 2026 was ordinary on its monthly
totals:

> **B1. The storm's freezing rain, not its total precipitation, set it apart from other winter
> storms.** Prompted by section 4 (the hourly file has a precipitation-type column) and section
> 5.3 (the monthly totals rank 21st of 30). *Refuted if* at least three earlier winters had a
> freezing-rain episode with as much liquid.

## In a student version only

Add a prompt for the student's own prediction before any data: "My prediction, before looking at
any data: ... and why". An analyst's deliverable does not include it.

*The analyst decides* the hypotheses in both sets.
