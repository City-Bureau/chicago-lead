hand_scrape_reports.processed.csv :
	python scripts/clean_hand_scrape_data.py > $@

tabula_reports.processed.csv : tabula-cps_lead_results.csv
	python scripts/clean_tabula_data.py $< > $@
 
output/cps_lead_scores.csv : hand_scrape_reports.processed.csv tabula_reports.processed.csv
	python scripts/score_schools.py $^ | python scripts/geocode_cps_lead_scores.py | \
	python scripts/add_missing_schools.py > $@

output/cps_lead.geojson : output/cps_lead_scores.csv
	csvjson --lat lat --lon long --crs urn:ogc:def:crs:OGC:1.3:CRS84 --indent 2 $< > $@

.PHONY: clean_schools
clean_schools :
	rm hand_scrape_reports.processed.csv tabula_reports.processed.csv all_schools.processed.csv