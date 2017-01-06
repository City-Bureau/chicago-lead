all : output/cps_lead_scores.geojson output/parks_lead_scores.csv output/water_projects.geojson 

include schools.mk parks.mk water_projects.mk

clean : 
	rm output/*