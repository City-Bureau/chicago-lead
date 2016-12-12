all: cps_lead.geojson

include schools.mk parks.mk water_projects.mk

clean:
	rm lead_scores.vrt hand_scrape_reports.processed.csv tabula_reports.processed.csv