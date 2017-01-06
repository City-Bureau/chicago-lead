# chicago-lead

How much lead is pouring out of Chicago's water fixtures, and where is it doing so in the highest amounts? 

To find out, we:

* Aggregate results from lead tests conducted in the city's schools and parks in 2016
* Geocode water main construction projects, which [shake loose the protective coating that keeps lead from leaching into water](http://southsideweekly.com/ground-zero/)

The results of this analysis appear in [a special issue of South Side Weekly](http://www.citybureau.org/lead/), powered by [City Bureau](http://www.citybureau.org/).

## Setup
### Dependencies
* python3 (we do some division that assumes that 1/2=0.5)
* csvkit (`pip install csvkit`)
* pyesridump (`pip install pyesridump`)

### Getting started

Clone this repo: 

**Using SSH**

`git clone git@github.com:datamade/chicago-lead.git`

**Using HTTPS**

`git clone https://github.com/datamade/chicago-lead.git`

Refer to **Data Docs** (below) for a description of the data.

### Replicating our work

To scrap the canned data and make it from scratch, run the following from a terminal window pointed at your project directory:

```
make clean
make all
```

The fresh data files will land in `output/`.

## Data Docs
Have an idea for further analysis? Here's the user manual for what we've done so far.

### 🌱 Parks

* **Files**
  * [parks_lead_scores.csv](output/parks_lead_scores.csv) contains three fields:

    * **park_name**: The name of the park
    * **num_fixtures**: The number of fixtures tested in the park
    * **score**: The proportion of fixtures tested that exceeded the EPA action level, 15 ppb. To calcuate this score, each test result was translated to a value, 0 if at or below 15 ppb, 1 if above. The park score is the average of its encoded fixture values.

* **Notes**

  * With a few isolated exceptions, parks fixtures were tested only once. We omitted retests and calcuated park scores based only on initial lead test results.

### 📚 Schools

* **Files**
  * [cps_lead_scores.geojson](output/cps_lead_scores.geojson) - Schools plotted by lat/long pairs, with attributes for:
    * **lead_score**: The proportion of fixtures tested that contained lead in excess of the EPA standard of 15 ppb. To calcuate, each trial was translated to a value, 0 for a measurement at or below the EPA standard, 1 for a measurement above it. The trials were averaged to produce a score for that fixture, then the fixture averages were averaged to produce a school-level score.
    * **num_fixtures**: The number of fixtures tested in a school
  
  * [cps_lead_scores.csv](output/cps_lead_scores.csv) - The above, in csv format (including lat/long)

* **Notes**
  * The above datasets contain results for 501 of 516 schools. The remaining 15 linked to dead files on the CPS site at the time of our analysis and thus could not be scraped. They are in our dataset with null values for score and fixture count:

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
  
  * The lat/long pairs were sourced from the data underlying [the lead map on the CPS site](http://cps.edu/Pages/LeadTesting.aspx).

### 💧 Water main projects

* **Files**

  * [water_projects.geojson](output/water_projects.geojson) - Planned & actual work on Chicago's water mains, from 2000 to present. Fields of interest include: 

    * **STARTDATE**: YYYY-MM-DD HH:MM:SS
    * **ENDDATE**: YYYY-MM-DD HH:MM:SS
    * **PLANNED_ACTUAL_FLAG**: Whether work is 'Planned' or 'Actual'
    * **FULL_ADDR**: Source address string for geocoding, i.e. 'ON N MANGO AVE FROM W FULLERTON AVE TO W GRAND AVE'
    * **PROJECT_DESC**: Short description of work to be done

## Errors and bugs

If something is not behaving intuitively, it is a bug and should be reported. Report it by [creating an issue](https://github.com/datamade/chicago-lead/issues).

Help us fix the problem as quickly as possible by following [Mozilla's guidelines for reporting bugs](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines#General_Outline_of_a_Bug_Report).

## Patches and pull requests

Your patches are welcome. Here's our suggested workflow:

* Fork the project.
* Make your feature addition or bug fix.
* Send us a pull request with a description of your work. Bonus points for topic branches!

## Copyright and attribution

Copyright (c) 2017 DataMade. Released under the [MIT License](LICENSE).
