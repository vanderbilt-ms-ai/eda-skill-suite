# EDA skill suite

Eleven Claude skills for exploratory data analysis (EDA) in Jupyter notebooks. They carry an analyst's
process from a stakeholder's problem to a finished pair of notebooks: one that gets and checks the
data, and one that tests hypotheses, writes new ones from what the data shows, and ends in a memo.
The skills do the mechanics and hand every judgment call back to the analyst.

Built for Vanderbilt University's DS 6120 (MS in AI program). The rules were drawn from two case
studies (the January 2026 Nashville ice storm and the 2020 presidential polls) and from test runs
on those cases and on College Scorecard data.

## The process

A request arrives with no data. The analyst writes the brief and the first hypotheses from the
request alone, each with the result that would refute it. The setup notebook finds the source,
downloads each piece once and checks it, renames the columns, inspects the data, and runs every
data-quality check. The analyst writes what those checks show as the second set of hypotheses, in
the same form, before any is tested. The analysis notebook tests each hypothesis as worded, and after
each verdict the analyst writes the next question as the next hypothesis. A regression, a clustering, or a
classifier is fitted to find the next cases to examine, not as the result. The notebook ends with
a synthesis, the limits, a memo, and a recap table. The process returns to the setup notebook
whenever a finding needs data it does not have.

The process draws on Zumel and Mount's data science workflow, Tukey's exploratory data analysis,
and Wickham's tidy data.

## The skills, and which rules each one owns

Each rule lives in exactly one skill. The others name the owner instead of restating the rule, so a
rule is changed in one place.

Each skill opens with what it takes in and what it produces.

| Skill | Takes in | Produces | Rules it owns |
|---|---|---|---|
| `eda-investigate` | the stakeholder's request | the project folder: two notebooks, `hypotheses.md`, `decisions.md`, `verification.md`, `data/` | the order of the stages; handing decisions back; doing the analysis in the notebook; the section with no hypothesis; returning for more data; where the next hypothesis comes from |
| `eda-hypothesis` | the analyst's request for help with a hypothesis, at any stage | a hypothesis in the analyst's words, or an evaluation of theirs | what a hypothesis contains; the questions that form or evaluate one. Runs only when the analyst asks |
| `eda-get-data` | `hypotheses.md` | the setup notebook, `data/raw/`, clean files, `PROVENANCE.md` | the source; the request; the first look; checks against known facts; provenance |
| `eda-check-data` | the setup notebook after its first look | the data-quality and preprocessing sections | every quality check, missing values and gaps in a series included; the section's budget; preprocessing |
| `eda-test-hypothesis` | one hypothesis and the clean data | one section of the analysis notebook | reading the claim; the analysis for each kind of claim; the verdict; the next hypothesis |
| `eda-model` | a hypothesis that needs a model | one model section | regression, clustering, classification; leakage; the four parts of a model section |
| `eda-verify` | the project folder | `verification.md` and the fixes | the verification steps |
| `eda-write-notebook` | any notebook | no file; rules for every cell | section structure; outputs that show results; column naming; size; code; runs top to bottom |
| `eda-draw-figure` | the data for one chart | one figure and its markdown | plot choice; titles, labels, ticks; integrity; color; matched pairs; the five-step description |
| `eda-write-prose` | any text about the analysis | no file; rules for every sentence | plain statements; observation before question; describe, interpret, conclude; words that match the data; length; emphasis; plain ASCII |
| `eda-scripts` | a notebook, a project folder, or a download list | lint output, a download table, PNG files, a pass/fail report | the four scripts |

## Installing

Paste this prompt into Claude Code:

```text
Install the EDA skill suite from https://github.com/vanderbilt-ms-ai/eda-skill-suite. Clone the
repository into a temporary folder, copy every folder under its skills/ directory into
~/.claude/skills/ (replace any older copies, including every older eda- folder and the old
notebook-standards, figure-standards, and writing-standards folders), then delete the temporary folder. Make sure the
Python packages pandas and nbformat are installed. Finish by listing the eleven installed skills.
```

- One project only: in that project, ask for the skills to go into `.claude/skills/` instead.
- Updating: paste the same prompt again.
- Without Claude Code: in Claude.ai, zip each folder under `skills/` and upload it under Settings,
  Capabilities, Skills. In other assistants, attach the `SKILL.md` files as instructions.

## Using the skills

Start a new Claude Code session so it picks up the skills, then describe the problem the way it
reached you:

```text
Here's an email from my director: "[the email]". I'm the data analyst. Help me investigate this in
a Jupyter notebook using [the data source].
```

Claude loads `eda-investigate`, which brings in the other skills at each stage and stops to ask at
each decision that belongs to the analyst.

## The tools

All scripts are in `skills/eda-scripts/scripts/` and need Python 3 and `pandas`:

| Script | What it does |
|---|---|
| `nb_lint.py NB.ipynb --trace` | errors for breaches a script can see (missing titles or labels, prose prints, sections without a finding, sections that test something without "Refuted if", cells not executed, non-ASCII, idioms); warnings for a person to read (framing sentences, reversals, wording beyond the record, cells over 200 words, and every quoted number that no output shows) |
| `fetch.py` | copied into the project as `tools/fetch.py`; fetches each piece once, checks the response before saving, retries, and reports a table of pieces |
| `figures.py NB.ipynb OUT/` | writes every figure to PNG so each one is looked at |
| `check_order.py DIR --stamp` and `check_order.py DIR` | records a hash and time for `hypotheses.md`, then checks the data was downloaded after it and the analysis notebook carries it verbatim |

## How the skills were tested, and what has not been

Before this version, each test gave an agent only a stakeholder's problem and no data, and checked
the two notebooks it produced against a finished case study: three complete runs on the ice storm
(NOAA weather records), two on College Scorecard, and one plain Claude Code session with the skills
installed and a student-style prompt, which loaded `eda-investigate` on its own and produced two
notebooks that passed the lint. Each round's failures became rules.

This version restructured the suite (one owner per rule, the scripts skill, the second set of hypotheses, the
added writing rules, the lint changes) and has not yet been run end to end. The next test should
be a problem of a different shape from the two cases the rules came from, such as a survey with
weights or an experiment, before the rules are trusted beyond weather series and institution
tables.

## Known limits

- Every test ran unattended, so the agent made every "the analyst decides" call itself. With a
  person in the loop the skills stop and ask instead; that path has not been tested.
- The lint's wording checks are pattern matches. They flag candidates; a person decides each one.
- `check_order.py` relies on a stamp written when `hypotheses.md` is finished. Without the stamp it
  falls back to file modification times, which a copy or a checkout can reset.
