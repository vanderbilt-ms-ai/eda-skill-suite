---
name: eda-write-prose
description: Writes text about data that a decision-maker who does not read code can act on: findings, memos, notebook markdown, figure titles, and summaries. Use whenever writing or reviewing any text about an analysis.
---

# How text about data is written

**Inputs.** Any text in the project: notebook markdown, a finding, the synthesis, the memo, the
recap, a figure title or label.

**Produces.** No file of its own. These rules apply to every sentence of both notebooks and the
memo. The reader is a decision-maker who does not read code: could they understand this without
looking up a term, does it answer the question they asked, and could they make a decision from
it? Every rule below makes one of those three more likely.

## Say the true thing plainly

- State what is true, directly. "Polls of every size missed by about 5 points on average" tells
  the reader something; "Size wasn't the story; place was" does not.
- Two constructions read as machine-written and are cut on sight: the reversal ("Not the size of
  the poll - but where it was taken") and the list of three ("Bigger samples, same miss, wrong
  theory"). Their rhythm carries no information.
- No slogans or idioms ("the perfect storm", "cry wolf", "smoking gun"). A metaphor stays only
  when it explains a mechanism. Teaching material has its own rules for analogies; these rules
  are for analysis prose.
- No figurative verbs: data does not "tell", "want", or "know"; a model does not "think"; words
  do not "carry" anything. Say what was measured and what it shows.
- No framing sentences. "This section looks at the storm hour by hour" and "This notebook finds
  the source and downloads the records" announce content instead of giving it. The heading
  already names the subject; start with the first fact.
- No filler: "It is worth noting that", "Interestingly", "In conclusion".
- Full sentences. Not "2020: +8.4 vs +4.4" and not "Twelve states, no change." Write "National
  polls put Biden ahead by 8.4 points on average; he won by 4.4."
- The field's own terms: "precipitation", not "water"; "margin of error", not "wiggle room".
  Define each term, statistic, and acronym at first use: "R-squared, the share of variation the
  model explains".
- Nothing the reader has not been given yet. A measure, a group, or a result is defined in the
  section that introduces it before a later section uses it.

## Observation before question

Before asking why, state what was observed: what was measured, by how much, compared with what.
Then word the question to match that observation and no broader. "National polls put Biden ahead
by 8.4 points on average; he won by 4.4" supports "Why were the polls off?"; it does not support
"What went wrong?"

## Findings: describe, interpret, conclude

Each finding makes three moves:

1. Describe what is visible, with its number: "The 225 polls from the final week overstated Biden
   by 3.5 points on average."
2. Interpret what it means in context: "Late polls missed less than mid-October polls, but in the
   same direction."
3. Conclude what follows for the question: the verdict (`eda-test-hypothesis`, section 3), or the
   next hypothesis.

A memo or report leads with the conclusion, then the evidence, then the method.

## Words that match the data

- Every claim carries its number, and the number is visible in a notebook output
  (`eda-write-notebook`, Cells show).
- Say what the data recorded, no more. "Freezing rain was reported", not "freezing rain fell",
  when the record is an observer's report. "The most of any January in the 30 requested", not
  "a record". A duration measured from readings, not a claim about what the readings did not
  measure.
- Every rank names the years it was computed over: "third of eleven Januaries".
- A blank is "not recorded", not "did not happen".
- No causal words without causal evidence. "Polls overstated Democrats more in states that voted
  more Republican", not "Republican voters caused the error". A regression shows association:
  write "moves with".
- No column names in prose, titles, or labels: "average error", not `abs_error_pts`. Markdown
  that teaches the code may name a column in backticks; findings, memos, titles, and labels do
  not.
- Translate a number into something a non-specialist can act on: "a poll ten times larger has
  about a third of the margin of error".
- Write every share the same way in one document: percent in prose and on axes, or shares in
  both.

## Length

- The opening markdown of a section: three to six sentences. A "What we found": two to five. A
  hypothesis: under 80 words (`eda-hypothesis`). A memo: one page.
- No markdown cell over about 200 words; the lint warns. A longer cell holds two ideas, so split
  it, or it narrates, so cut it.

## Emphasis and characters

- Bold marks the labels ("**What we found.**", "**Analyst decision.**") and the verdicts. Nothing
  else is bold.
- Plain ASCII punctuation: a hyphen, never an em dash or an en dash; "to" or "then", never an
  arrow; straight quotes; no ellipsis character. A degree sign is acceptable in a figure; in
  prose write "degrees F".

## Reference

- `references/examples.md`: sentences from drafts and test runs, each with the problem named and
  the rewrite. Read it when a sentence is in doubt.
