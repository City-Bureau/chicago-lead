clean_scrape.csv : tabula-Water_Fountain_Testing_Final_Results.csv
	sed -e '1s/^/fixture_location,result=/' $< | tr '=' '\n' | \
	sed -e 's/^\("",\)*//' -e 's/\(,""\)\{2,\}/,""/' -e 's/,"",/,/' -e 's/ ,/,/' | \
	csvsql --query "select * from stdin where fixture_location not in ('Indoor', 'Outdoor', 'Oudoor')" | \
	python scripts/clean_parks.py > $@

output/parks_lead_scores.csv : clean_scrape.csv
	python scripts/score_parks.py $< > $@

.PHONY: clean_parks
clean_parks :
	rm clean_scrape.csv