---
name: eda-write-hypotheses
description: Writes the brief, the questions, and the hypotheses of an investigation, before any data (series A) and again from what the data shows (series B), each with what would refute it. Owns the hypothesis rules. Use at the start of an analysis and whenever a finding raises a question worth testing.
---

# Write the hypotheses

A question worth the reader's time is written as a hypothesis with its refutation before it is
tested. This skill owns the brief and every rule about hypotheses; `eda-get-data` builds the
setup notebook, and `eda-test-hypothesis` tests what is written here.

## The brief (first cell of the analysis notebook)

- Who the analyst is, who is asking, and what situation prompted it.
- The observation, stated before any question (`eda-write-prose`, Observation before
  question). Write it first as the stakeholder reports it. After the pull, the setup notebook
  computes the observation's numbers in its last section, "The numbers the brief quotes", and the
  brief is updated to cite them. The questions do not change when the numbers arrive.
- The stakeholder's request, quoted.
- The question or questions it reduces to.

*The analyst decides* the questions.

## Hypotheses

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
into the analysis notebook verbatim; `eda-scripts/scripts/check_order.py` checks the file predates
the data.

**Series B: after looking.** The first look and the data-quality checks show distributions, gaps,
groups, and ranges that the problem statement could not. Each later finding does the same. A
question those views raise is written as a series B hypothesis, in the same form, before its
section runs, with one more line: what prompted it (the view, the table, or the finding). The first
batch is written in the analysis notebook right after the data-quality section is read, under its
own heading; later ones open the digging-deeper section that tests them. Series B hypotheses are
numbered B1, B2, and so on.

The two series serve different purposes. Series A tests what people already believe, and a failed
series A hypothesis stays failed (`eda-test-hypothesis`, The verdict); a better measure that
turns up later is a series B hypothesis, not a repair. Series B is the investigation: it carries the
questions the data itself raised, and it is where most findings come from.

In a student version only, add a prompt for the student's own prediction before any data. An
analyst's deliverable leaves it out.

*The analyst decides* the hypotheses in both series.

