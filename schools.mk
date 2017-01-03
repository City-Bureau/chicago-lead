.INTERMEDIATE : fusion.csv
fusion.csv : raw/cps_lead_fusion_table.csv
	perl -p -e 's/Individualschool_Falconer_609910/Individualschool_Falconer_609910.pdf/' $< | \
	perl -p -e 's/4,LEAD FOUND,IndividualSchool_Williams_610380.pdf/4,LEAD FOUND,None/' > $@

.INTERMEDIATE : measured_cps_lead_scores.csv
measured_cps_lead_scores.csv : get-the-lead-out/cps.csv
	cat $< | python scripts/cps_score.py > $@

output/cps_lead_scores.csv : fusion.csv measured_cps_lead_scores.csv 
	csvjoin -c "Filename","filename" --left $^ | \
	csvcut -c "SchoolName","score","num_fixtures","Lat","Long" > $@

output/cps_lead_scores.geojson : output/cps_lead_scores.csv 
	csvjson --lat Lat --lon Long --crs urn:ogc:def:crs:OGC:1.3:CRS84 --indent 2 $^ > $@