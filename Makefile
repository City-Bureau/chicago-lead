all : output/cps_lead.geojson output/parks_lead_scores.csv output/water_projects_all_years.geojson clean 

include schools.mk parks.mk water_projects.mk

clean : clean_schools clean_parks clean_water_projects