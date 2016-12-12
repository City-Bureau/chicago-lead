all: cps_lead.geojson

hand_scrape_reports.processed.csv:
	python scripts/clean_hand_scrape_data.py > $@

tabula_reports.processed.csv:
	python scripts/clean_tabula_data.py tabula_reports.raw.csv > $@
 
lead_scores.csv: hand_scrape_reports.processed.csv tabula_reports.processed.csv
	python scripts/score_schools.py $^ t > $@
	python scripts/add_missing_schools.py

cps_lead.geojson: lead_scores.csv
	python scripts/generate_vrt.py $(basename $<) > $(basename $<).vrt
	ogr2ogr -f "GeoJSON" cps_lead.geojson $(basename $<).vrt

clean:
	rm lead_scores.vrt hand_scrape_reports.processed.csv tabula_reports.processed.csv