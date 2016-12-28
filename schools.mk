hand_scrape.clean.csv : 
	python scripts/clean_hand_scrape.py > $@

tabula.clean.csv : tabula/tabula-cps_lead_results.csv
	perl -p -e 's|,pdf.$$|,filename|; s|http:.*LeadTesting/||' $< > $@.tmp
	echo "\nZapata,1-E-CS02-51,Room 105 - North,6/3/16 6:50 AM,27.6,Individualschool_Zapata_609973.pdf\n\
	Orr,51558-1-HAL-F05,\"Main- Next to Room 118, Fountain\",10/12/16 6:00 AM,530,IndividualSchool_Orr_610389.pdf" >> $@.tmp
	csvsort $@.tmp | python scripts/clean_tabula.py > $@
 
cps_lead_scores.csv : hand_scrape.clean.csv tabula.clean.csv
	csvstack $^ | python scripts/cps_score.py

cps_lead.geojson : cps_lead_scores.csv
	csvjson --lat lat --lon long --crs urn:ogc:def:crs:OGC:1.3:CRS84 --indent 2 output/$< > output/$@

.PHONY : clean_schools
clean_schools :
	rm *.clean.csv *.tmp