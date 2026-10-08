---
name: eda-write-prose
description: Keeps writing about data plain, precise, and supported by the numbers, in notebook markdown, findings, memos, figure text, and summaries. Owns every prose rule in the suite. Use whenever writing or reviewing text about an analysis.
---

# Writing standards

The reader is a decision-maker who does not read code (the general-manager test): could they
understand this without searching for any term, does it answer the question they asked, and could
they make a decision from it? Write so the answer to all three is yes. These rules govern analysis
prose: notebook markdown, findings, synthesis, memo, recap, and the text on figures.

## Say the true thing plainly

- Prefer the direct statement of what is true. "Polls of every size missed by about 5 points on
  average" beats "Size wasn't the story; place was."
- No aphorisms. Two constructions read as machine-written and are cut on sight: the reversal
  ("Not the size of the poll - but where it was taken") and the rule of three ("Bigger samples,
  same miss, wrong theory"). Neither tells the reader anything.
- No slogans, taglines, or catchphrases ("the perfect storm", "the data tells a story"). A
  metaphor or analogy stays only if it explains a mechanism; an idiom ("cry wolf", "smoking gun")
  never does. Teaching material has its own rules for analogies; this rule is for analysis prose.
- No figurative language and no personification: the data does not "want", "tell", or "know"; a
  model does not "think". Say what was measured and what it shows.
- No framing sentences. A sentence that announces what a section, notebook, or paragraph is about
  to do ("This section looks at the storm hour by hour"; "This notebook finds the source and pulls
  the records") says nothing the heading did not. Start with the content.
- No filler or throat-clearing: "It is worth noting that", "Interestingly", "In conclusion".
- Full sentences, never fragments or shorthand: "National polls put Biden ahead by 8.4 points on
  average; he won by 4.4", not "2020: +8.4 vs +4.4" and not "Twelve states, no change."
- The field's terms ("precipitation", not "water"; "margin of error", not "wiggle room"), each
  term and every statistic and acronym defined at first use ("R-squared, the share of variation
  the model explains").
- Nothing the reader has not been given yet: a measure, a group, or a result is defined in the
  section that introduces it before any later section relies on it.

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
3. Conclude what follows for the question: the verdict (`eda-test-hypothesis`, The verdict), or
   the next hypothesis.

In a memo or report, lead with the conclusion (conclusion, evidence, method).

## Words that match the data

- Every claim carries its number, and the number traces to an output in the notebook
  (`eda-write-notebook`, Cells show).
- Say what the data recorded, not more: "freezing rain was reported", not "freezing rain fell",
  when the record is an observer's report; "the most of any January in the 30 pulled", not "a
  record"; a duration measured from readings, not a claim about what the readings did not measure.
- Every rank carries its window: "third of eleven Januaries".
- A blank is "not recorded", not "did not happen".
- No causal words without causal evidence: "polls overstated Democrats more in states that voted
  more Republican", not "Republican voters caused the error". A regression shows association;
  write "moves with".
- No variable names in prose, titles, or labels: "average error", not `abs_error_pts`.
  Code-explaining markdown may name a column in backticks when it is teaching the code; findings,
  memos, titles, and labels never do.
- Translate numbers into something a non-specialist can act on: "a poll ten times larger has
  about a third of the margin of error".
- Write every share the same way in one document (percent in prose and on axes, or shares in
  both).

## Length

- Opening markdown of a section: three to six sentences. A "What we found": two to five. A memo:
  one page.
- No markdown cell over about 200 words; the lint warns. A longer cell is two ideas, so split it,
  or it is narration, so cut it.

## Emphasis and characters

- Bold marks labels ("**What we found.**", "**Analyst decision.**") and verdicts, nothing else.
- Plain ASCII punctuation: a hyphen, never an em dash or en dash; "to" or "then", never an arrow;
  straight quotes; no ellipsis character. The degree sign in a unit is acceptable in figures; in
  prose write "degrees F".

## Reference

- `references/examples.md`: sentences from case-study drafts, before and after.
