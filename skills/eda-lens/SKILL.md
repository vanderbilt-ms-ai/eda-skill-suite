---
name: eda-lens
description: Uses regression, clustering, and classification in the middle of an analysis to find what to investigate next. Use whenever an analysis calls for a model.
---

# Models as lenses

In exploration a model is usually a way of looking one layer deeper, not the end of the analysis.
Fit it, check it is sound, and then read what it surfaces: those cases are the next questions. Each
lens section of the analysis notebook follows `notebook-standards` (opening markdown, chart and
table, "What we found") and ends with "**Next questions.**"

## Before any model

- **Say why this lens, for this question**, in the opening markdown: what the model will show that
  the summaries could not.
- **Choose the variables from the question**, not from whatever columns exist. Say what each
  measures and why it belongs.
- **Check the rows the model will use** (complete cases) against `eda-data-quality`'s missingness
  findings: if the complete rows differ from the rest, the model describes only them. Say so.
- Define every statistic at first use (slope, intercept, r, R-squared, silhouette, accuracy,
  precision, recall).

## Regression

- Fit with a formula (`smf.ols("y ~ x", data=df).fit()`); report the **slope in the data's units**
  ("1.5 points more error for every 10 points more Republican"), the intercept's meaning (the value
  where x is 0, if 0 is meaningful), r, and R-squared. Put them on the chart.
- Log-transform a predictor that spans orders of magnitude, and say what the slope then means
  ("per tenfold increase").
- **Residuals are the lens**: list the largest positive and negative residuals with the cases'
  names. Next question: what do the cases that beat the prediction share?
- **Compare blocks of variables** by R-squared (how it was run vs where it was taken) to see which
  explains more.
- **Check the pattern where the event did not happen** (another year, another group) before calling
  it a cause.
- A regression shows association. Write "moves with", not "causes".

## Clustering

- Features tied to the question. **Scale** them (`StandardScaler`) when their units differ; do not
  when they share a unit.
- k-means with a fixed seed and several starts (`KMeans(n_clusters=k, n_init=20, random_state=0)`).
- **Choose k deliberately**: compute the silhouette score (how much closer each case is to its
  own group than to the next, from -1 to 1) and the inertia (elbow) for k = 2 to 8, and show both.
  Start from the k with the highest silhouette. Choose a different k only when its silhouette is
  within 0.05 of the best and its groups are easier to describe, and show both profiles. Say why.
- **Profile each cluster**: the mean of each feature, the count, and an outcome the clustering did
  not use. Cross-tabulate clusters against any known label. Name each cluster by its profile.
- Next questions: what do the members share that the features did not include? Do the groups
  differ on an outcome they were not built from?
- Hierarchical clustering (Ward linkage) is a check on whether the groups are stable.

## Classification

- **Define the label** and why it matters for the decision.
- **"In advance" means only what was known before the outcome.** Every feature must be measured
  before the outcome period; a feature derived from the outcome, or measured after it, is leakage
  and makes the classifier look better than it is. Make a table of each feature and when it is
  known.
- **Features chosen by looking at every row leak too.** Features named in the hypotheses, before
  the data was pulled, are fine. If earlier sections chose further features by comparing the label
  across all rows, the test rows helped choose them. Split first and choose
  features on the training rows only, or say the test is optimistic.
- **Very few positives** (fewer than about 20): a train/test split leaves too few to test. Use
  leave-one-out (fit on all cases but one, predict that one, repeat), or evaluate on all cases and
  label the result in-sample. A rule whose thresholds were fixed in the hypotheses before the data
  was pulled is not fitted, so it can be evaluated on every case.
- **Rare positives** (the label is under about 10 percent of cases): report the class balance; use
  `class_weight="balanced"` or choose the probability threshold on the training rows; judge the
  model by precision and recall, not accuracy (always guessing "no" is already accurate). A case at
  a probability of exactly 0.50 can be classified differently by two libraries; report it as on the
  boundary.
- **Baseline first**: the accuracy of always predicting the most common class.
- **Split before anything else** (`train_test_split`, stratified on the label); fit any scaling on
  the training rows only; touch the test rows once. To try a feature the misses suggest, compare
  models by cross-validation on the training rows (`cross_val_score`), then score the chosen model
  on the test rows once.
- **When every available feature was measured after the outcome** (a single recent release), the
  classifier cannot show what was knowable in advance. Either pull an earlier release for the
  features (*the analyst decides*: it may be a large download), or keep the verdict at **supported,
  not proven** and say why.
- **Precision and recall in one hypothesis**: fix one as the setting and test the other ("at the
  setting that catches 80 percent of the cases, at least half of the flags are right"). That is one
  claim.
- Models: logistic regression (read coefficients as changes in the odds), k-nearest neighbors; a
  threshold rule counts as a classifier too.
- **Report the confusion matrix**, accuracy, precision, and recall, and say which error matters
  more for this decision.
- **The misses are the lens**: list the misclassified cases. Next question: what is different
  about them?
- **Overfitting check**: a rule or threshold chosen after seeing the case will flag the case. Test
  it on cases not used to set it (another period, held-out rows), or say it is untested.

## Output of every lens section

1. Chart (scatter with line; clusters colored; confusion matrix) and a labelled table.
2. "**What we found.**" with the numbers.
3. "**What the lens surfaced.**" - the specific cases (largest residuals, cluster profiles,
   misclassified cases).
4. "**Next questions.**" - two or three, each tied to a surfaced case.

*The analyst decides* the target and features, k, whether the groups mean anything, and which
surfaced case to chase.

## Reference

- `references/lens-examples.md` - the three lenses as used in the 2020 polls case.
