---
name: eda-hypothesis
description: Helps the analyst form a hypothesis, or evaluates one they already have, by asking questions until it is one claim with a stated refutation. Use only when the analyst asks for help with a hypothesis, at any point before, during, or after an analysis.
---

# Help with a hypothesis

**Inputs.** The analyst's request, in one of two forms: "help me form a hypothesis about ..." or
"evaluate this hypothesis: ...". Whatever exists at that point: nothing, the setup notebook, or
findings in the analysis notebook.

**Produces.** A hypothesis in the analyst's words that meets the form below, confirmed by the
analyst, or an evaluation of their hypothesis with one question per thing missing. The analyst
puts it where it belongs: `hypotheses.md` before any data, or the analysis notebook after.

This skill runs only when the analyst asks for it. `eda-investigate` does not call it; the
hypotheses in an investigation are the analyst's own, and the other skills refer to this file
for the form. The skill asks; it does not write a hypothesis for the analyst, because a
hypothesis the analyst did not form is not theirs to defend.

## What a hypothesis contains

- One claim, as a full sentence that could be false. A claim with several parts ("the month was
  cold and wet and windy") is split into one hypothesis per part, each with its own verdict.
- "Refuted if", followed by the result that would refute it. A claim with no such result is not
  a hypothesis.
- The smallest difference that would change the stakeholder's decision, not only its direction:
  "refuted if the gain does not recover the extra cost within 10 years", not "refuted if the gain
  is zero or less". A claim about a rank ("the worst in years") is tested by the rank among named
  years and needs no margin.
- Under 80 words, from its label to its last word. A longer one holds two claims or the argument
  for the claim; the argument goes in the section that tests it.
- A number, in the order it will be tested, within its question.
- When it tests a word of the request, the word and what it requires: "pays off" requires a gain
  compared with its cost; "the worst in years" requires named years; "could we have told in
  advance" requires only what was known before the outcome.
- When it was written after looking at data: one line naming what prompted it (the table, the
  chart, or the finding, by section). Hypotheses written from the request alone are numbered H1,
  H2, ...; hypotheses written after looking are numbered B1, B2, ... so a reader can tell which
  beliefs came before the data.

## Forming a hypothesis

Ask these one at a time, and wait for each answer. Do not skip ahead to a draft.

1. Which question is this hypothesis for, and what does the stakeholder's request say about it,
   in their words?
2. What do you believe the answer is? Who else believes it, and why? (A belief the stakeholder or
   their colleagues already hold is the first thing to test; a mechanism you thought of yourself
   usually needs a look at the data first.)
3. Have you looked at any data yet? If so, what did you see that made you think of this? (That
   decides whether it is an H or a B hypothesis, and gives the "prompted by" line.)
4. If your belief is right, what would the data show? Which measure, compared with what, over
   which cases or years?
5. If your belief is wrong, what would the data show instead? (This becomes "Refuted if".)
6. How big would the difference have to be to change what the stakeholder does?
7. Does the data you have, or can get, measure that? If not, what is the closest measure, and
   what does the substitution cost?

Then read back one hypothesis assembled from the analyst's own sentences, labelled "In your
words:", with the word count, and ask them to confirm or change it. Use their phrasing; do not
rewrite it into the analyst's voice as you imagine it, and do not add a claim, a measure, or a
threshold they did not state. If the answers hold no claim yet, say so and ask for one. If they
hold two claims, say so and ask which one this hypothesis is.

## Evaluating a hypothesis

Check the hypothesis against each line of the form and report every check, pass or fail, in a
short table. For each fail, ask the one question whose answer fixes it, rather than rewriting the
hypothesis. The questions that come up most:

| Fail | Question to ask |
|---|---|
| More than one claim | Which claim is this hypothesis about? The other becomes its own. |
| No refutation | What result would make you give this up? |
| Direction only, no size | How much of a difference would change the decision? |
| 80 words or more | Which words are the claim, and which are the argument for it? |
| A mechanism written before any data ("it is a genre artifact") | What have you seen that suggests it? If nothing yet, would you hold it until after the first look? |
| A threshold chosen from the case it flags | Would you test it on cases that did not set it, or say it is untested? |
| A rank with no years named | Which years is this rank among? |
| A measure the data does not hold ("streams" when the file holds a popularity score) | Will you test the closest measure under its own name, and record the substitution? |
| A word of the request not tested as worded ("pays off" tested as "more goes with more") | What does that word require, and does the test compare that? |

End with the analyst's hypothesis as they last stated it and the checks that still fail, if any.
The verdict on a tested hypothesis is not this skill's job; that is `eda-test-hypothesis`.
