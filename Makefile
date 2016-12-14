all : output/cps_lead.geojson output/parks_lead_scores.csv clean 

include schools.mk parks.mk water_projects.mk

clean : clean_schools clean_parks