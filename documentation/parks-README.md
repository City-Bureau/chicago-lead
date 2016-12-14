# data directory

1. [chi-parks-lead-scores.processed.csv](https://github.com/datamade/chicago-lead/blob/master/assets/chi-parks-lead-results/chi-parks-lead-scores.processed.csv) is scores aggregated to park level as discussed.

2. [parks_score_lookup_table.csv](https://github.com/datamade/chicago-lead/blob/master/assets/chi-parks-lead-results/parks_score_lookup_table.csv) is the same score data with an additonal `geo_name` column that corresponds to the names in the city's aug 2012 parks shapefile for easy joining, if you please. (this omits parks in the test result data that did not have a corresponding shape in the shapefile.) 

3. [chi-parks-lead-results-10-2016.processed.csv](https://github.com/datamade/chicago-lead/blob/master/assets/chi-parks-lead-results/chi-parks-lead-results-10-2016.processed.csv) is the raw results data plus two calculated fields, `processed_result` which converts `result_value` to numbers by converting the below-threshold (<.120 etc.) readings to 0, and `exceeds_epa` which is 0 for results at or below the 15ppb threshold and 1 for results above it.
