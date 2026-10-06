---
name: eda-workflow
description: Runs an exploratory data analysis (EDA) from a stakeholder's problem to finished Jupyter notebooks, calling the other EDA skills at each stage and handing judgment calls back to the analyst. Use whenever someone brings a problem, question, or dataset to investigate.
---

# EDA workflow

This skill runs the whole exploratory data analysis process and calls the other skills at each
stage. It does the mechanics; the analyst makes the judgment calls.

## The process

The data science workflow (Zumel and Mount) runs define the goal, collect and manage, build the
model, evaluate and critique, present and document, deploy - and it loops ("loops within loops").
**EDA is not a single stage between collecting data and modelling**: it runs across
collect-and-manage, build, and evaluate. It organizes the
data, spots problems, and identifies which modelling strategies are even available.

Inside the loop, every move applies Tukey's two principles: **simplify** on purpose (and notice
what the simplification drops), then **look one layer deeper** ("the mean is 47 - fine, what is the
distribution?"). A case-study investigation follows a steady arc: state the
hypotheses before looking at data; test each one ("Is that unusual? How do we check?"); when the
obvious answers fail, ask "so what happened?" and dig one level deeper at a time; the explanation
is often a combination nobody hypothesized.

Clustering, regression, and classification are usually **lenses inside the loop**, not its end: a
regression's residuals ask who beats the prediction; a cluster asks what its members share; a
classifier's misses ask what is different about them. Each of those results points to the next
question to investigate. A model is the end of the analysis only when building it was the goal.

## Stages and skills

| Stage | Skill | The analyst decides |
|---|---|---|
| 1a. Problem to questions: brief, observation, questions, hypotheses and what would refute each, written **before any data is pulled** | `eda-notebook-setup` | the question, the hypotheses, the size of difference that matters |
| 1b. Find, size, and pull the data once; first look | `eda-notebook-setup` | the source, the window, the unit of analysis |
| 2. Data quality: what a row is, missing values, values and units, coverage, preprocessing | `eda-data-quality` | what each problem means and what to do about it (drop, keep, impute, narrow the scope) |
| 3. Test each hypothesis as worded; dig deeper | `eda-analysis-selection` (+ `figure-standards`) | whether the test matches the claim; the verdict; which question comes next |
| 4. Models as lenses | `eda-lens` | the target and features; k; whether groups mean anything; which surfaced cases to chase |
| 5. Synthesis, limits, memo | `writing-standards` | the interpretation, the recommendation |
| 6. Verify | `eda-verify` | sign-off |

`notebook-standards`, `figure-standards`, and `writing-standards` apply to every cell at every
stage. Read them before writing the first cell.

## Deliverables

Two notebooks in the project folder, plus the data:

1. `<case>-step0-get-the-data.ipynb` - sections in this order: where the data comes from; naming
   conventions; the request(s), each piece downloaded once and checked; first look (inspection and
   the three sentences); data quality (every check from `eda-data-quality`, each with "What we
   found"); checks against facts you already know; save and provenance; the numbers the brief
   quotes. Writes `data/` (raw downloads unchanged in `data/raw/`, cleaned files,
   `PROVENANCE.md`).
2. `<case>-analysis.ipynb` - brief; setup cell (imports and loading the saved data); hypotheses
   (written before the data was pulled); one section per hypothesis test, in the hypotheses'
   numbered order; "Something else?"; digging deeper, one step per section, each ending with the
   next question; lens sections where a model directs the next step; synthesis; limits; the memo;
   a recap table (question | hypothesis | what the data showed).

## Handing decisions back

At every point marked "the analyst decides":
- **Working with a person:** stop and ask, with the options and what each would change.
- **Running unattended** (no one to ask): make the choice a careful analyst would make, write it in
  the notebook where it applies as a short "**Analyst decision.**" paragraph (what was decided, the
  alternative, why), and add it to `decisions.md` beside the notebooks. Never hide a decision in
  code.

## The notebook is where the investigation happens

Do the exploring in the notebooks, in order, one section at a time: write the section's opening
markdown and code, run it, read the output, then write its "What we found" from that output. Do
not work the analysis out in side scripts or a scratch session and then transcribe the conclusions
into a notebook, and never write a finding (or a placeholder number to fill in later) before the
output it cites exists. A notebook assembled afterwards reads like an investigation without having
been one: its sections follow the conclusion instead of leading to it, and its findings are not
tied to the outputs above them. Small checks on how a file is formatted, before the request is
written, are fine; anything that looks at the values the questions are about belongs in a notebook
section.

## "Something else?"

After the opening hypotheses are tested, one section looks at the case itself with no hypothesis:
the same measures at a finer grain (the event's days instead of the month; one state instead of the
nation), and the case's rank on a few measures nobody named. It lists what stands out, adds the
next questions the hypothesis sections already raised, and ends with the candidate list and the one
chosen. Each later digging-deeper section starts from one of them.

## Where derived tables are built

A derived table the hypotheses define before any data (one row per event, per state, per institution)
is built in the setup notebook's preprocessing and saved. A table that a later finding calls for is
built in the analysis section that needs it.

## The data-quality stage does not test the hypotheses

Stage 2 looks at one variable at a time, at missing values, and at how the data was recorded. It
does not plot the outcome against the variables the hypotheses name, and it does not compute the
comparison a hypothesis makes. Those belong to stage 3, after the hypotheses are fixed.

## Going back to the setup notebook

The process loops back. When the analysis needs a column, a period, or a check the setup notebook does not have
(a classifier's misses point at a kind of case nobody flagged), go back: add it to the setup
notebook in the section where it belongs (the request, a data-quality check, preprocessing), pull
only the addition, re-run the setup notebook, then re-run the analysis notebook from the top. Record
the loop in `decisions.md` (what was added and which finding sent you back) and mention it in the
analysis section that needed it.

## Digging deeper: where the next question comes from

After each finding, list candidate next questions and pick one (or ask). The standard moves:
- Is that unusual? Compared with what, over the same window?
- The maximum (or the minimum) instead of the total.
- When did it happen within the period? (day, then hour)
- What was the other variable doing at the same time? (build matched pairs in the same form)
- How long did it last? What accumulated?
- Up for whom? Does the aggregate hide subgroups that differ?
- Does the pattern also appear where the event did not happen? (before calling it the cause)
- What does the model's residual, cluster, or miss point at?

## Finish

Run `eda-verify`. Then `notebook-standards/scripts/nb_lint.py <nb> --trace` on both notebooks
must report 0 errors, and every figure must have been looked at.
