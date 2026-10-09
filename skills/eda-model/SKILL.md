---
name: eda-model
description: Fits a regression, a clustering, or a classifier in the middle of an analysis and lists the cases it surfaces, for the analyst's next hypotheses. Use whenever a hypothesis calls for a model.
---

# Fitting a model in the middle of the analysis

**Inputs.** A hypothesis whose test needs a model (`eda-test-hypothesis`, section 2), the clean
data, and the missingness findings from `eda-check-data`.

**Produces.** One section of the analysis notebook with the four parts listed at the end of this
file. In this course a model used this way is called a lens: it is fitted to find the cases to
examine next, not as the result of the analysis. A model is the result only when building it was
the stakeholder's request.

## Before any model

- Write in the opening markdown what the model will show that the summaries could not.
- Choose the variables from the hypothesis, not from the columns that happen to exist. Say what
  each measures and why it belongs.
- Compare the rows the model will use with the rest, using the missingness findings
  (`eda-check-data`, Missing values, item 7). If the complete rows differ from the rest, the model
  describes only the complete rows. Say so.
- Define each statistic at first use (`eda-write-prose`): slope, intercept, r, R-squared,
  silhouette, inertia, accuracy, precision, recall.

## Regression

- Fit with a formula: `smf.ols("y ~ x", data=df).fit()`. Report the slope in the data's units
  ("1.5 points more error for every 10 points more Republican"), the intercept's meaning when x = 0
  is meaningful, r, and R-squared. Put the slope and r on the chart.
- Take the log of a predictor that spans orders of magnitude, and say what the slope then means
  ("per tenfold increase").
- List the largest positive and the largest negative residuals with the cases' names. The
  question to put to the analyst: what do the cases above the line share, or the cases below it?
- Compare blocks of variables by R-squared to see which block explains more.
- Before calling a pattern the cause of an event, fit the same model where the event did not
  happen (another year, another group). Wording: `eda-write-prose`, Words that match the data.

## Clustering

- Use features the hypothesis names. Scale them with `StandardScaler` when their units differ; do
  not scale when they share a unit.
- Use k-means with a fixed seed and several starts: `KMeans(n_clusters=k, n_init=20,
  random_state=0)`.
- Show the silhouette score and the inertia for k from 2 to 8. Start from the k with the highest
  silhouette. Choose another k only when its silhouette is within 0.05 of the best and its groups
  are easier to describe; show both profiles and say why.
- Profile each cluster: the mean of each feature, the count, and an outcome the clustering did not
  use. Cross-tabulate the clusters against any known label. Name each cluster by its profile.
- The questions to put to the analyst: what do the members of a cluster share that the features
  did not include; do the clusters differ on an outcome they were not built from?
- Hierarchical clustering with Ward linkage checks whether the groups are stable.

## Classification

- Define the label and say why it matters for the decision.
- "In advance" means every feature was measured before the outcome. A feature derived from the
  outcome, or measured after it, is leakage and makes the classifier look better than it is.
  Make a table of each feature and when it is known.
- Features chosen by comparing the label across every row leak too. Features named in the first
  set of hypotheses are safe. If earlier sections chose features by looking at every row, split
  first and choose features on the training rows only, or say the test is optimistic.
- Fewer than about 20 positive cases: a train/test split leaves too few to test. Use leave-one-out
  (fit on all cases but one, predict that one, repeat), or evaluate on all cases and label the
  result in-sample. A rule whose thresholds were fixed before the data was downloaded is not
  fitted, so it can be evaluated on every case.
- Positives under about 10 percent of cases: report the class balance; use
  `class_weight="balanced"` or choose the probability threshold on the training rows; judge the
  model by precision and recall, not accuracy, because always predicting "no" is already accurate.
  A case at a probability of exactly 0.50 is classified differently by different libraries;
  report it as on the boundary.
- Report the baseline first: the accuracy of always predicting the most common class.
- Split before anything else, with `train_test_split` stratified on the label. Fit any scaling on
  the training rows only. Score the test rows once. To try a feature the misses suggest, compare
  models by cross-validation on the training rows (`cross_val_score`), then score the chosen
  model on the test rows once.
- If every available feature was measured after the outcome, the classifier cannot show what was
  knowable in advance. Either download an earlier release for the features (*the analyst
  decides*; it may be large) or keep the verdict at supported, not proven, and say why.
- A hypothesis about precision and recall fixes one and tests the other: "at the setting that
  catches 80 percent of the cases, at least half of the flags are right".
- Models: logistic regression (a coefficient is a change in the odds); k-nearest neighbors; a
  threshold rule counts as a classifier.
- Report the confusion matrix, accuracy, precision, and recall, and say which error costs more
  for this decision.
- List the misclassified cases. The question to put to the analyst: what is different about them?
- A rule or threshold chosen after seeing the case will flag the case. Test it on cases that did
  not set it (another period, held-out rows), or say it is untested.

## The four parts of a model section

1. The chart (scatter with its line; clusters colored; confusion matrix) and a labelled table.
2. "**What we found.**", with the numbers.
3. "**What the model surfaced.**": the specific cases (the largest residuals, the cluster
   profiles, the misclassified cases).
4. "**Next hypotheses.**": the analyst's, two or three, each about one surfaced case, in the form
   `eda-hypothesis` sets. Ask the analyst for them; do not write them.

*The analyst decides* the target and the features, the number of clusters, whether the groups mean
anything, and which surfaced case to examine next.

## Reference

- `references/lens-examples.md`: the three models as used in the 2020 polls case.
