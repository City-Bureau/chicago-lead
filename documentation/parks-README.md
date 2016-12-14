# chicago parks lead scores

## to reproduce

in a terminal window, run:

`make output/parks_lead_scores.csv`
`make clean_parks`

## data dir

1. [parks_lead_scores.csv](https://github.com/datamade/chicago-lead/blob/master/output/parks_lead_scores.csv) contains three fields:

  * **park_name**: the name of the park
  * **num_fixtures**: the number of fixtures tested in the park
  * **score**: the proportion of fixtures tested that exceeded the epa action level, 15 ppb. to calcuate this score, each test result was translated to a value, 0 if at or below 15 ppb, 1 if above. the park score is the average of its encoded fixture values.

## notes

* with a few isolated exceptions, parks fixtures were tested only once. we omitted retests and calcuated park scores based only on initial lead test results.