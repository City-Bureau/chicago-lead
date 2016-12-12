hand_scrape_reports.processed.csv:
	python scripts/clean_hand_scrape_data.py > $@

tabula_reports.processed.csv: tabula-cps_lead_results.csv
	python scripts/clean_tabula_data.py $< > $@
 
output/lead_scores.csv: hand_scrape_reports.processed.csv tabula_reports.processed.csv
	python scripts/score_schools.py $^ | python scripts/geocode_cps_lead_scores.py | \
	python scripts/add_missing_schools.py > $@

output/cps_lead.geojson: lead_scores.csv
	python scripts/generate_vrt.py $(basename $<) > $(basename $<).vrt
	ogr2ogr -f "GeoJSON" $@ $(basename $<).vrt