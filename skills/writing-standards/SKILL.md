---
name: writing-standards
description: The rules for every sentence an analysis produces - notebook markdown, findings, figure titles, memos, and reports - plain direct statements, no aphorisms or catchy phrasing (the reversal, the rule of three, slogans), no variable names in prose, the observation stated before the question, findings in describe-interpret-conclude form with the number that decides them, words that match what the data shows, and plain ASCII. Use this skill whenever you write or review prose for a data analysis, including a "What we found" cell, a memo to a stakeholder, a figure title, or a summary, even a single sentence.
---

# Writing standards

The reader is a decision-maker who does not read code (the general-manager test): could they understand
this without searching for any term, does it answer the question they asked, and could they make a
decision from it? Write so the answer to all three is yes.

## Say the true thing plainly

- **Prefer the direct statement of what is true.** "Polls of every size missed by about 5 points on
  average" beats "Size wasn't the story; place was."
- **No aphorisms.** Two constructions read as machine-written and are cut on sight:
  - **The reversal**: "Not the size of the poll - but where it was taken", "Trace claims to the
    paper - until one doesn't trace". It sounds profound and tells the reader nothing.
  - **The rule of three**: "Bigger samples, same miss, wrong theory", "Your notes, your words, the
    data open". The rhythm carries no information the reader can use.
- **No slogans, taglines, or catchphrases**: "the perfect storm", "the data tells a story", "it's
  not the size, it's the timing", "numbers don't lie". A metaphor stays only if it explains a
  mechanism.
- **No filler or throat-clearing**: "It is worth noting that", "Let's dive in", "Interestingly",
  "In conclusion", "At the end of the day". Start with the content.
- **Full sentences, not shorthand**: "National polls put Biden ahead by 8.4 points on average; he
  won by 4.4", not "2020: +8.4 vs +4.4".
- **The field's terms, defined at first use**: "margin of error", not "wiggle room"; "R-squared (the share
  of variation the model explains)". Define every acronym on first use.

## Observation before question

Before asking why, state what was observed, specifically: what was measured, by how much, compared
with what. Then word the question to match that observation and no broader. "National polls put
Biden ahead by 8.4 points on average; he won by 4.4" supports "Why were the polls off?"; it does not
support "What went wrong?"

## Hypotheses and verdicts

- A hypothesis is a sentence that could be false. Before keeping one, name the result that would
  refute it.
- Test it **exactly as worded**: a claim about the month is tested with monthly numbers. If it
  fails, say so; a different measure is a new question, not a rescue ("depends on the measure",
  "partly holds" are not verdicts).
- Verdicts are bold and plain: **Hypothesis 2 does not hold.** / **holds.** / **is supported, not
  proven** (when the evidence fits but cannot rule out the alternatives, or the test was tuned on
  the case it flags).
- A result exactly on the refutation line is decided by the refutation as written ("refuted if
  fewer than three": three holds). State the result and the line together.

## Findings: describe, interpret, conclude

Each finding makes three moves (describe, interpret, conclude):

1. **Describe** what is literally visible, with its number: "The 225 polls from the final week
   overstated Biden by 3.5 points on average."
2. **Interpret** what it means in context: "Late polls missed less than mid-October polls, but in
   the same direction."
3. **Conclude** what follows for the question: "**Hypothesis 3 does not hold:** the final week's
   polls were not accurate."

In a memo or report, lead with the conclusion (the inverted pyramid: conclusion, evidence, method).

## Words that match the data

- **Every claim carries its number**, and the number traces to an output in the notebook.
- **Say what the data recorded, not more**: "[the event] was reported", not "[the event] happened"
  when the record is an observer's report; "the most of any [case] in [the window pulled]", not "a
  record"; a duration measured from readings, not a claim about what the readings did not measure.
- **Every rank carries its window**: "third of eleven Januaries", "the highest of 30 years". A rank
  depends on the window pulled; a longer record can move it.
- **A blank is "not recorded"**, not "did not happen".
- **No causal words without causal evidence**: "polls overstated Democrats more in states that voted
  more Republican", not "Republican voters caused the error".
- **No variable names in prose, titles, or labels**: "field goal percentage", not `pctFG`; "average
  error", not `abs_error_pts`. Code-explaining markdown may name a column in backticks when it is
  teaching the code; findings, memos, titles, and labels never do.
- Translate numbers into something a non-specialist can act on: "a poll ten times larger has about
  a third of the margin of error".

## Characters

Plain ASCII punctuation: a hyphen, never an em dash or en dash; "to" or "then", never an arrow;
straight quotes. The degree sign in a unit (degrees F) is acceptable in figures; in prose, write
"degrees F" or "°F" consistently within one document.

## Reference

- `references/examples.md` - sentences from case-study drafts, before and after.
- `../notebook-standards/scripts/nb_lint.py` flags non-ASCII punctuation, variable names in
  findings, stock phrases, and short punchy sentences for review.
