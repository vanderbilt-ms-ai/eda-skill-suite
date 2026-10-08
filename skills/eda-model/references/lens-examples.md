# The three lenses in the 2020 polls case

## Regression pointed to the next question

1. A regression of each state's average poll error on how the state voted: slope -0.15, r = -0.70.
   Read alone, it says Republican states were polled worse.
2. Lens step: does the pattern appear where the event did not happen? The same regression for 2012
   gave slope -0.16, r = -0.73 - the same pattern in an election the polls did not miss.
3. Next question, from that: fit the line for every election and compare the two numbers. The slope
   was normal in every election; the error where the race was even moved from between -1.6 and
   +0.2 (2000-2012) to +3.6 (2016) and +4.2 (2020). The finding was that the line's level moved while its slope stayed the same.

## Clustering found groups built only from the past

- Features: each state's average poll error in 2012 and in 2016 (same unit, so no scaling).
- k chosen by silhouette (0.50 for two groups, 0.52 for three) and readability: two.
- Profile: the group that missed in 2016 (16 states) overstated the Democrat by 5.7 points in
  2016; the other group by -0.8.
- The outcome the clustering did not use: in 2020 the first group's polls overstated Biden by 5.6,
  the second's by 1.8. Groups formed before 2020 were 3.7 points apart in 2020.

## Classification showed which way the misses went

- Each poll treated as a classifier of its state's winner.
- As published: 76.7% of polls picked the winner; the confusion matrix showed 163 polls that wrongly
  picked Biden and 52 that wrongly picked Trump.
- A correction (subtract the 2016 average error) raised accuracy to 80.5% but traded one error for
  the other: 55 wrong Biden picks, 125 wrong Trump picks.
- The misses: the state correction called every state but Georgia. Next question: what was
  different about Georgia?
