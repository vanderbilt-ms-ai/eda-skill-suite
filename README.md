# EDA skill suite

Nine Claude skills for exploratory data analysis (EDA) in Jupyter notebooks. They carry an
analyst's process from a stakeholder's problem to a finished pair of notebooks: one that gets and
checks the data, and one that tests hypotheses, digs deeper, and ends in a memo. The skills do the
mechanics and hand every judgment call back to the analyst.

Built for Vanderbilt University's DS 6120 (MS in AI program) and tested on two case studies: the
January 2026 Nashville ice storm and the 2020 presidential polls.

## The process

A problem arrives with no data. The analyst writes the questions and the hypotheses, including what
would refute each one, before opening any data. The setup notebook finds the source, pulls each
piece once and checks it, renames columns, and runs the first look and every data-quality check,
missing values included. The analysis notebook tests each hypothesis as worded, digs one level
deeper at a time when the obvious explanations fail, and uses regression, clustering, and
classification as lenses that point to the next question. It ends with a synthesis, the limits,
a memo, and a recap table. The process loops back to the setup notebook whenever a finding needs
data it does not have.

The process draws on Zumel and Mount's data science workflow, Tukey's exploratory data analysis,
and Wickham's tidy data.

## The skills

Workflow skills, one per stage:

| Skill | What it does |
|---|---|
| `eda-workflow` | Runs the whole investigation and calls the other skills at each stage |
| `eda-notebook-setup` | Turns the problem into questions and hypotheses; pulls, checks, and documents the data |
| `eda-data-quality` | Checks data quality, including missing values, and records each decision |
| `eda-analysis-selection` | Chooses the analysis and figure that test each hypothesis; states the verdict and the next question |
| `eda-lens` | Uses regression, clustering, and classification to find what to investigate next |
| `eda-verify` | Re-runs the analysis and confirms every number, word, and figure matches the data |

Standards skills, applied to every cell:

| Skill | What it does |
|---|---|
| `notebook-standards` | Keeps notebooks clear, reproducible, and easy to follow; `scripts/nb_lint.py` checks what it can |
| `figure-standards` | Creates figures that follow best practices for communicating insights visually |
| `writing-standards` | Keeps writing about data plain, precise, and supported by the numbers |

## Installing

Paste this prompt into Claude Code:

```text
Install the EDA skill suite from https://github.com/vanderbilt-ms-ai/eda-skill-suite. Clone the
repository into a temporary folder, copy every folder under its skills/ directory into
~/.claude/skills/ (replace any older copies of the same skills), then delete the temporary folder.
Make sure the Python package nbformat is installed, since the notebook-standards lint script needs
it. Finish by listing the nine installed skills.
```

- **One project only:** in that project, ask for the skills to go into `.claude/skills/` instead of
  `~/.claude/skills/`.
- **Updating:** paste the same prompt again.
- **Without Claude Code:** in Claude.ai, zip each folder under `skills/` and upload it under
  Settings, Capabilities, Skills. In other assistants, attach the `SKILL.md` files as instructions.

## Using the skills

Start a new Claude Code session so it picks up the skills, then describe the problem the way it
reached you, for example:

```text
Here's an email from my director: "[the email]". I'm the data analyst. Help me investigate this in
a Jupyter notebook using [the data source].
```

Claude loads `eda-workflow`, which brings in the other skills at each stage and stops to ask you at
each decision that belongs to the analyst.

## The lint script

```bash
python skills/notebook-standards/scripts/nb_lint.py NOTEBOOK.ipynb --trace
```

It reports errors (missing titles or axis labels, prose print statements, sections without a
finding, cells not executed) and warnings for a person to check, including any number in a finding,
the brief, the memo, or the recap that does not appear in an output. It needs Python 3 and
`nbformat`.

## How the skills were tested

Each test gave an agent only a stakeholder's problem and no data, and checked the two notebooks it
produced against a finished case study:

- three complete runs on the January 2026 Nashville ice storm, using NOAA weather records;
- two complete runs on College Scorecard data, a question about college price and earnings that
  needs regression, clustering, and classification;
- one plain Claude Code session with the skills installed and a student-style prompt. It loaded
  `eda-workflow` on its own and followed it through the other skills to two notebooks that pass the
  lint.

Each round's failures became rules. Examples: opening hypotheses written after looking at the data;
the same files downloaded twice; one missing hour shortening a "hours in a row" count; notebooks
twice the size of the examples; findings worked out in side scripts and written into the notebook
afterwards.

## Known limits

- The tests ran unattended, so the agent made every "the analyst decides" call itself. With a
  person in the loop, the skills stop and ask instead; that path has not been tested.
- The last rule added (do the analysis in the notebook, and write each finding only after its
  output exists) has not been retested.
