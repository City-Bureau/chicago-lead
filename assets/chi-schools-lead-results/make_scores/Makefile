all: cps_lead_scores.geojson

hand_scrape_reports.processed.csv:
	python scripts/clean_hand_scrape_data.py > $@

tabula_reports.processed.csv:
	python scripts/clean_tabula_data.py tabula_reports.raw.csv > $@
 
lead_scores.csv: hand_scrape_reports.processed.csv tabula_reports.processed.csv
	python scripts/score_schools.py $^ t > $@

cps_lead.geojson: lead_scores.csv
	python scripts/generate_vrt.py $(basename $<) > $(basename $<).vrt
	ogr2ogr -f "GeoJSON" cps_lead.geojson $(basename $<).vrt

clean:
	rm lead_scores.csv lead_scores.vrt hand_scrape_reports.processed.csv tabula_reports.processed.csv