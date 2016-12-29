.PHONY: schools
schools : cps_lead_scores.csv cps_lead.geojson

hand_scrape.clean.csv : 
	python scripts/clean_hand_scrape.py > $@

tabula.clean.csv : tabula/tabula-cps_lead_results.csv
	perl -p -e 's|,pdf.$$|,filename|; s|http:.*LeadTesting/||' $< > $@.tmp
	echo "\nZapata,1-E-CS02-51,Room 105 - North,6/3/16 6:50 AM,27.6,Individualschool_Zapata_609973.pdf\n\
	Orr,51558-1-HAL-F05,\"Main- Next to Room 118, Fountain\",10/12/16 6:00 AM,530,IndividualSchool_Orr_610389.pdf" >> $@.tmp
	csvsort $@.tmp | python scripts/clean_tabula.py > $@

fusion.clean.csv : raw/cps_lead_fusion_table.csv
	perl -p -e 's|Individualschool_Falconer_609910|Individualschool_Falconer_609910.pdf|;\
	s|4,LEAD FOUND,IndividualSchool_Williams_610380.pdf|4,LEAD FOUND,None|' $< > $@
 
output/cps_lead_scores.csv : hand_scrape.clean.csv tabula.clean.csv fusion.clean.csv
	csvstack $< $(word 2,$^) | csvsql --query "select distinct SchoolName, sample, location, date, result, s.filename \
	from '$(basename $(word 3,$^))' as f left join stdin as s on (f.Filename=s.filename)" --no-inference $(word 3,$^) | \
	python scripts/cps_score.py > $@

output/cps_lead.geojson : output/cps_lead_scores.csv fusion.clean.csv
	csvsql --query "select s.school_name, s.score, s.num_fixtures, f.lat, f.long from $(notdir $(basename $<)) as s \
	join '$(basename $(word 2,$^))' as f on (upper(s.school_name)=f.SchoolName)" --no-inference $< $(word 2,$^) | \
	csvjson --lat Lat --lon Long --crs urn:ogc:def:crs:OGC:1.3:CRS84 --indent 2  > $@

.PHONY : clean_schools
clean_schools :
	rm *.clean.csv *.tmp
