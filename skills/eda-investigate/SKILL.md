---
name: eda-investigate
description: Runs an exploratory data analysis from a stakeholder's request to two finished Jupyter notebooks and a memo, calling the other eda- skills at each stage. Use when someone brings a problem or question to investigate with data.
---

# The investigation from request to memo

**Inputs.** A stakeholder's request (an email, a message, a question) and, sometimes, a data
source the stakeholder names. Nothing else exists at the start: no data, no notebooks.

**Produces.** A project folder holding:
- `<case>-step0-get-the-data.ipynb`, the setup notebook: finds the source, downloads the data,
  renames columns, inspects the data, runs the quality checks, and saves clean files to `data/`.
- `<case>-analysis.ipynb`, the analysis notebook: the brief, the hypotheses, one section per
  test, the model sections, the synthesis, the limits, the memo, and the recap table.
- `hypotheses.md` (the first hypotheses, written before any data), `decisions.md` (every judgment
  call), `verification.md` (the verification report), and `data/` (raw downloads unchanged in
  `data/raw/`, clean files, `PROVENANCE.md`).

The other skills hold the rules for each stage. This file holds the order of the stages, what the
analyst decides at each, and the rules that belong to no single stage.

## The stages, in order

| Stage | Skill | The analyst decides |
|---|---|---|
| 1. The analyst writes the brief and the first hypotheses from the request alone, before any data exists; record them in `hypotheses.md` and stamp it | the analyst; `eda-hypothesis` if they ask for help | the questions; the hypotheses; the smallest difference that matters |
| 2. Find the source, download the data once, rename, inspect | `eda-get-data` | the source; the years or entities to request; the unit of analysis |
| 3. Run the data-quality checks and the preprocessing | `eda-check-data` | what each problem means and what to do about it |
| 4. The analyst writes the second set of hypotheses from what stages 2 and 3 showed, under "## Second hypotheses (from the data)" | the analyst; `eda-hypothesis` if they ask for help | which to test, in what order |
| 5. Test each hypothesis as worded; after each verdict, the analyst writes the next hypothesis | `eda-test-hypothesis` | whether the test matches the claim; the verdict; the next hypothesis |
| 6. Fit a model where a hypothesis calls for one, and read what it surfaces | `eda-model` | the target and features; the number of clusters; which surfaced cases to examine |
| 7. Write the synthesis, the limits, the memo, and the recap | `eda-write-prose` | the interpretation; the recommendation |
| 8. Verify everything against the data | `eda-verify` | sign-off |

Load each stage's skill with the Skill tool before writing that stage's first cell, even when
the stage looks familiar. The rules that decide a verdict, a model, or a figure are in those
files and nowhere else; a run that skipped `eda-test-hypothesis` and `eda-model` produced
verdicts and classifiers that followed neither.

Three skills apply to every cell at every stage: `eda-write-notebook` (how a notebook is built),
`eda-draw-figure` (how a figure is drawn), and `eda-write-prose` (how text about data is written).
Load all three before the first cell. `eda-scripts` holds the scripts the stages run.

## Handing decisions back

At every point a skill marks "the analyst decides":
- With a person present: stop and ask. Give the options and what each would change. Ask only
  decisions the conversation has not already settled.
- When the analyst answers, write the decision in the notebook where it applies as a paragraph
  labelled "**Analyst decision.**" (what was decided, the alternative, why), and add it to
  `decisions.md`. A decision made inside code and not written down is a breach.
- When no one answers, stop and list what is needed. Do not make the analyst's decisions; a
  notebook whose hypotheses and choices the analyst did not make is not theirs to defend. (Test
  harnesses supply a stand-in analyst; that is the harness's job, not a rule here.)

## Do the analysis in the notebook

Build each section in order: write its opening markdown and code, run the code, read the output,
then write "What we found" from that output. Do not compute results in a side script or a
scratch session and copy the conclusions into the notebook afterwards. Do not write a finding, or
a placeholder number, before the output it cites exists. A check on how a file is formatted,
before the request is written, may run outside the notebook; a look at the values the questions
are about may not. The re-derivation in `eda-verify` runs in a separate script on purpose: it
checks the notebook after the fact.

## The section with no hypothesis

After the first hypotheses (stage 5) are tested, one section examines the case itself: the same
measures at a finer level of detail (the event's days instead of the month; one state instead of
the nation), and the case's rank on a few measures nobody named. It lists what stands out, adds
the second-set hypotheses not yet tested, and ends with the list of candidates and the one chosen.
The analyst writes the chosen candidate as a hypothesis (form in `eda-hypothesis`), and the next section starts from it.

## Where derived tables are built

A table the first hypotheses already define (one row per event, per state, per institution) is
built and saved in the setup notebook's preprocessing section. A table a later hypothesis needs is
built in the analysis section that tests it.

## Going back for more data

When a test needs a column, a period, or a check the setup notebook lacks: add it to the setup
notebook in the section where it belongs, download only the addition, re-run the setup notebook,
then re-run the analysis notebook from the top. Record in `decisions.md` what was added and which
finding needed it, and say so in the analysis section that needed it.

## Where the next hypothesis comes from

After each finding, list candidate next questions and choose one. The usual sources:
- Is the value unusual? Compared with what, over the same period?
- The maximum or the minimum instead of the total.
- When within the period did it happen? The day, then the hour.
- What was the other variable doing at the same time? Draw both in the same form, side by side
  (`eda-draw-figure`, Matched pairs).
- How long did it last? What accumulated?
- Do subgroups differ in ways the total does not show?
- Does the same pattern appear where the event did not happen?
- What do the model's residuals, clusters, or misclassified cases point at? (`eda-model`)

Put the candidates to the analyst. The analyst chooses one and writes it as a hypothesis (form in
`eda-hypothesis`) before its section runs.

## Finish

Run `eda-verify`. Both notebooks report 0 errors from `nb_lint.py --trace`, `check_order.py`
passes, and every figure has been opened and looked at (`eda-scripts`).
