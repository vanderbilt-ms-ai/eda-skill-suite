---
name: eda-lens
description: Uses regression, clustering, and classification in the middle of an analysis to find what to investigate next. Use whenever an analysis calls for a model.
---

# Models as lenses

In exploration a model is a way of looking one layer deeper, not the end of the analysis. Fit it,
check it is sound, then read what it surfaces: those cases are the next hypotheses. Each lens
section has the three parts every section has (`eda-notebook-standards`, Structure) and ends with
"**Next hypotheses.**" (`eda-notebook-setup`, Hypotheses, series B).

## Before any model

- Say why this lens, for this question, in the opening markdown: what the model will show that the
  summaries could not.
- Choose the variables from the question, not from whatever columns exist. Say what each measures
  and why it belongs.
- Check the rows the model will use against the missingness findings (`eda-data-quality`, Missing
  values, item 7). If the complete rows differ from the rest, the model describes only them. Say
  so.
- Statistics are defined at first use (`eda-writing-standards`); the ones this skill needs are
  slope, intercept, r, R-squared, silhouette, inertia, accuracy, precision, and recall.

## Regression

- Fit with a formula (`smf.ols("y ~ x", data=df).fit()`); report the slope in the data's units
  ("1.5 points more error for every 10 points more Republican"), the intercept's meaning when x = 0
  is meaningful, r, and R-squared. Put slope and r on the chart.
- Log-transform a predictor that spans orders of magnitude, and say what the slope then means
  ("per tenfold increase").
- Residuals are the lens: list the largest positive and negative residuals with the cases' names.
  Next hypothesis: what the cases that beat the prediction share.
- Compare blocks of variables by R-squared to see which explains more.
- Check the pattern where the event did not happen before calling it a cause; the wording rule is
  in `eda-writing-standards` (Words that match the data).

## Clustering

- Features tied to the question. Scale them (`StandardScaler`) when their units differ; do not
  when they share a unit.
- k-means with a fixed seed and several starts (`KMeans(n_clusters=k, n_init=20, random_state=0)`).
- Choose k deliberately: show the silhouette score and the inertia for k = 2 to 8. Start from the k
  with the highest silhouette. Choose a different k only when its silhouette is within 0.05 of the
  best and its groups are easier to describe, and show both profiles. Say why.
- Profile each cluster: the mean of each feature, the count, and an outcome the clustering did not
  use. Cross-tabulate clusters against any known label. Name each cluster by its profile.
- Next hypotheses: what the members share that the features did not include; whether the groups
  differ on an outcome they were not built from.
- Hierarchical clustering (Ward linkage) is a check on whether the groups are stable.

## Classification

- Define the label and why it matters for the decision.
- "In advance" means only what was known before the outcome. Every feature must be measured before
  the outcome period; a feature derived from the outcome, or measured after it, is leakage. Make a
  table of each feature and when it is known.
- Features chosen by looking at every row leak too. Features named in series A hypotheses are
  fine. If earlier sections chose further features by comparing the label across all rows, split
  first and choose features on the training rows only, or say the test is optimistic.
- Very few positives (fewer than about 20): a train/test split leaves too few to test. Use
  leave-one-out, or evaluate on all cases and label the result in-sample. A rule whose thresholds
  were fixed before the data was pulled is not fitted, so it can be evaluated on every case.
- Rare positives (under about 10 percent): report the class balance; use
  `class_weight="balanced"` or choose the probability threshold on the training rows; judge by
  precision and recall, not accuracy. A case at a probability of exactly 0.50 can be classified
  differently by two libraries; report it as on the boundary.
- Baseline first: the accuracy of always predicting the most common class.
- Split before anything else (`train_test_split`, stratified on the label); fit any scaling on the
  training rows only; touch the test rows once. To try a feature the misses suggest, compare
  models by cross-validation on the training rows, then score the chosen model on the test rows
  once.
- When every available feature was measured after the outcome, the classifier cannot show what was
  knowable in advance. Either pull an earlier release for the features (*the analyst decides*), or
  keep the verdict at supported, not proven, and say why.
- Precision and recall in one hypothesis: fix one as the setting and test the other. That is one
  claim.
- Models: logistic regression (read coefficients as changes in the odds), k-nearest neighbors; a
  threshold rule counts as a classifier too.
- Report the confusion matrix, accuracy, precision, and recall, and say which error matters more
  for this decision.
- The misses are the lens: list the misclassified cases. Next hypothesis: what is different about
  them.
- Overfitting check: a rule or threshold chosen after seeing the case will flag the case. Test it
  on cases not used to set it, or say it is untested.

## Output of every lens section

1. Chart and a labelled table.
2. "**What we found.**" with the numbers.
3. "**What the lens surfaced.**": the specific cases (largest residuals, cluster profiles,
   misclassified cases).
4. "**Next hypotheses.**": two or three series B hypotheses, each tied to a surfaced case, each
   with its refutation.

*The analyst decides* the target and features, k, whether the groups mean anything, and which
surfaced case to chase.

## Reference

- `references/lens-examples.md`: the three lenses as used in the 2020 polls case.
