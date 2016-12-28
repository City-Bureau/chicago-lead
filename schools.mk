schools : 
	createdb $@
	csvsql --db postgresql:///$@ --table cps_fusion --insert raw/cps_lead_fusion_table.csv

hand_scrape_results : schools
	python scripts/clean_hand_scrape.py | \
	csvsql --db postgresql:///schools --blanks --no-inference --table $@ --insert

tabula_results : tabula/tabula-cps_lead_results.csv
	perl -p -e 's|,pdf.$$|,filename|; s|http:.*LeadTesting/||' $< > clean.csv
	echo "\nZapata,1-E-CS02-51,Room 105 - North,6/3/16 6:50 AM,27.6,Individualschool_Zapata_609973.pdf\n\
	Orr,51558-1-HAL-F05,\"Main- Next to Room 118, Fountain\",10/12/16 6:00 AM,530,IndividualSchool_Orr_610389.pdf" >> clean.csv
 
cps_lead_scores.csv : hand_scrape_results tabula_results
	psql -d schools -c "select * into all_results from (select * from tabula_results union all select * from hand_scrape_results) as tmp"

cps_lead.geojson : cps_lead_scores.csv
	csvjson --lat lat --lon long --crs urn:ogc:def:crs:OGC:1.3:CRS84 --indent 2 output/$< > output/$@

clean_schools :
	dropdb schools
	rm clean.csv