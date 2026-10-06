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

| Skill | Stage |
|---|---|
| `eda-workflow` | Runs the whole process; says which skill handles each stage and what the analyst decides |
| `eda-notebook-setup` | Problem to brief, questions, and hypotheses; find, size, and pull the data; first look; provenance |
| `eda-data-quality` | What a row is, missing values, values and units, coverage, preprocessing; every check reported |
| `eda-analysis-selection` | From a hypothesis as worded to the analysis and figure that test it; the verdict; the next question |
| `eda-lens` | Regression, clustering, and classification used mid-investigation to find what to ask next |
| `eda-verify` | Re-run, lint, trace and re-derive numbers, check the wording, look at every figure |

Standards skills, applied to every cell:

| Skill | Covers |
|---|---|
| `notebook-standards` | Section structure, explanation before each test, results as charts and labelled tables, naming, simple code, size; `scripts/nb_lint.py` checks what it can |
| `figure-standards` | Plot type, titles, labels, ticks, reference lines, integrity, color, the five-step figure description |
| `writing-standards` | Plain statements without aphorisms or slogans, observation before question, describe-interpret-conclude, words that match the data, plain ASCII |

## Installing

- **Claude Code:** copy the folders under `skills/` into `~/.claude/skills/` (every project) or a
  project's `.claude/skills/`.
- **Claude.ai:** zip each skill folder and upload it under Settings, Capabilities, Skills.
- **Other assistants:** attach the relevant `SKILL.md` files as instructions.

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
