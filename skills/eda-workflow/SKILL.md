---
name: eda-workflow
description: Runs an exploratory data analysis (EDA) from a stakeholder's problem to finished Jupyter notebooks, calling the other EDA skills at each stage and handing judgment calls back to the analyst. Use when someone brings a problem, question, or dataset to investigate in a notebook.
---

# EDA workflow

This skill owns the arc of the investigation: the stages, which skill runs each one, the
deliverables, and how decisions are handed back. Each rule in the suite lives in one skill; this
file points to the owner rather than restating the rule.

## The process

The data science workflow (Zumel and Mount) runs define the goal, collect and manage, build the
model, evaluate and critique, present and document, deploy, and it loops ("loops within loops").
EDA runs across collect-and-manage, build, and evaluate: it organizes the data, spots problems, and
identifies which modelling strategies are available.

Inside the loop, every move applies Tukey's two principles: simplify on purpose (and notice what
the simplification drops), then look one layer deeper ("the mean is 47; what is the
distribution?"). The investigation is a chain of questions. Each look at the data produces the
next question, and a question worth the reader's time is written as a hypothesis with its
refutation before it is tested (`eda-notebook-setup`, Hypotheses). Clustering, regression, and
classification are lenses inside the loop (`eda-lens`), and a model is the end of the analysis
only when building it was the goal.

## Stages and skills

| Stage | Skill | The analyst decides |
|---|---|---|
| 1a. Problem to brief, questions, and the first hypotheses (series A), written before any data is pulled | `eda-notebook-setup` | the questions, the hypotheses, the size of difference that matters |
| 1b. Find, size, and pull the data once; first look | `eda-notebook-setup`, `eda-tools` (fetch) | the source, the window, the unit of analysis |
| 2. Data quality: what a row is, missing values, values and units, coverage, preprocessing | `eda-data-quality` | what each problem means and what to do about it |
| 2b. Hypotheses from the first look (series B): what the univariate views and the quality checks suggest, written as hypotheses with refutations before they are tested | `eda-notebook-setup`, Hypotheses | which of them to test and in what order |
| 3. Test each hypothesis as worded; after each verdict, the next question, as a series B hypothesis | `eda-analysis-selection` | whether the test matches the claim; the verdict; the next hypothesis |
| 4. Models as lenses | `eda-lens` | the target and features; k; whether groups mean anything; which surfaced cases to chase |
| 5. Synthesis, limits, memo | `eda-writing-standards` | the interpretation, the recommendation |
| 6. Verify | `eda-verify`, `eda-tools` | sign-off |

`eda-notebook-standards`, `eda-figure-standards`, and `eda-writing-standards` apply to every cell
at every stage. Read them once, before the first cell, and keep them open.

## Deliverables

Two notebooks in the project folder, plus the data and three small files:

1. `<case>-step0-get-the-data.ipynb`: where the data comes from; naming conventions; the request,
   each piece fetched once and checked; first look; data quality (every check from
   `eda-data-quality`); checks against facts already known; save and provenance; the numbers the
   brief quotes. Writes `data/` (raw downloads unchanged in `data/raw/`, cleaned files,
   `PROVENANCE.md`).
2. `<case>-analysis.ipynb`: brief; setup cell; series A hypotheses (inserted verbatim from
   `hypotheses.md`); series B hypotheses from the first look; one section per hypothesis test, in
   numbered order; "Something else?"; digging-deeper sections, each testing a series B hypothesis;
   lens sections; synthesis; limits; the memo; a recap table (question, hypothesis, what the data
   showed).
3. `hypotheses.md` (series A, written before the request runs; `eda-tools/scripts/check_order.py`
   checks that it predates the data), `decisions.md` (every analyst decision, see below), and
   `verification.md` (`eda-verify`).

## Handing decisions back

At every point a skill marks "the analyst decides":
- Working with a person: stop and ask, with the options and what each would change. Ask only real
  decisions; never offer an option that contradicts what the person already said.
- Running unattended: make the choice a careful analyst would make, write it in the notebook where
  it applies as a short "**Analyst decision.**" paragraph (what was decided, the alternative, why),
  and add it to `decisions.md`. Never hide a decision in code.

## The notebook is where the investigation happens

Do the exploring in the notebooks, in order, one section at a time: write the section's opening
markdown and code, run it, read the output, then write its "What we found" from that output. Do
not work the analysis out in side scripts or a scratch session and transcribe the conclusions
afterwards, and never write a finding, or a placeholder number, before the output it cites exists.
A notebook assembled afterwards reads like an investigation without having been one. Small checks
on how a file is formatted, before the request is written, are fine; anything that looks at the
values the questions are about belongs in a notebook section. (`eda-verify` re-derives numbers in
a separate script on purpose; that is a check on the notebook, not a place to do the analysis.)

## "Something else?"

After the series A hypotheses are tested, one section looks at the case itself with no hypothesis:
the same measures at a finer grain (the event's days instead of the month; one state instead of
the nation), and the case's rank on a few measures nobody named. It lists what stands out, adds the
open series B hypotheses, and ends with the candidate list and the one chosen. Each later
digging-deeper section starts from one of them, written as a hypothesis.

## Where derived tables are built

A derived table the series A hypotheses define before any data (one row per event, per state, per
institution) is built in the setup notebook's preprocessing and saved. A table a later hypothesis
calls for is built in the analysis section that needs it.

## Going back to the setup notebook

When the analysis needs a column, a period, or a check the setup notebook does not have, go back:
add it to the setup notebook in the section where it belongs, fetch only the addition
(`eda-tools` fetch skips pieces already on disk), re-run the setup notebook, then re-run the
analysis notebook from the top. Record the loop in `decisions.md` (what was added and which
finding sent you back) and mention it in the analysis section that needed it.

## Where the next question comes from

After each finding, list candidate next questions and pick one (or ask). The standard moves:
- Is that unusual? Compared with what, over the same window?
- The maximum (or the minimum) instead of the total.
- When did it happen within the period? (day, then hour)
- What was the other variable doing at the same time? (matched pairs in the same form,
  `eda-figure-standards`)
- How long did it last? What accumulated?
- Up for whom? Does the aggregate hide subgroups that differ?
- Does the pattern also appear where the event did not happen? (before calling it the cause)
- What does the model's residual, cluster, or miss point at? (`eda-lens`)

The chosen question becomes the next series B hypothesis, with its refutation, before its section
runs.

## Finish

Run `eda-verify`. Both notebooks must report 0 errors from `eda-tools/scripts/nb_lint.py --trace`,
`check_order.py` must pass, and every figure must have been looked at
(`eda-tools/scripts/figures.py`).
