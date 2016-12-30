# chicago-lead

how much lead is pouring out of chicago's fixtures?

## requirements
* csvkit (`pip install csvkit`)
* pyesridump (`pip install pyesridump`)

## to reproduce

clone this repo and from a terminal window, run:

`make all`

the files should land in `output/`.

## data docs

### 🌱 parks

#### to reproduce

in a terminal window, run:

`make output/parks_lead_scores.csv`

`make clean_parks`

#### output

1. [parks_lead_scores.csv](output/parks_lead_scores.csv) contains three fields:

  * **park_name**: the name of the park
  * **num_fixtures**: the number of fixtures tested in the park
  * **score**: the proportion of fixtures tested that exceeded the epa action level, 15 ppb. to calcuate this score, each test result was translated to a value, 0 if at or below 15 ppb, 1 if above. the park score is the average of its encoded fixture values.

#### notes

* with a few isolated exceptions, parks fixtures were tested only once. we omitted retests and calcuated park scores based only on initial lead test results.

### 📚 schools

#### to reproduce

in a terminal window, run:

`make output/cps_lead.geojson`

`make clean_schools`

#### contents

* [cps_lead.geojson](../output/cps_lead.geojson) - schools plotted by lat/long pairs, with attributes for:
  * **lead_score**: the proportion of fixtures tested that contained lead in excess of the epa standard of 15 ppb. to calcuate, each trial was translated to one of two values: 0 for a measurement at or below the epa standard, 1 for a measurement above it. the trials were averaged to produce a score for that fixture, then the fixture averages were averaged to produce a school-level score.
  * **num_fixtures**: the number of fixtures tested in a school
  
* [cps_lead_scores.csv](../output/cps_lead_scores.csv) - the above, in csv format

#### notes

* the above datasets contain results for 501 of 516 schools. the remaining 15 link to dead files on the cps site and thus could not be scraped. they are in our dataset with null values for score and fixtures:

  * Hoyne
  * Melody
  * Brownell
  * Mcauliffe
  * Decatur
  * Kipp Chicago - Ascend Primary
  * Jordan
  * Leland
  * Voise Hs
  * Casals
  * Bronzeville Hs
  * Lorca
  * Black
  * Christopher
  * Poe
  
* the lat/long pairs were sourced from the data underlying [the lead map on the cps site](http://cps.edu/Pages/LeadTesting.aspx).
