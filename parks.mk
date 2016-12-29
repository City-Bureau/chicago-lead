clean_scrape.csv : tabula/tabula-Water_Fountain_Testing_Final_Results.csv
	perl -p -e 'print "fixture_location,result\n" if $$. == 1' $< | \
	perl -p -e 's/^("",)*//; s/(,""){2,}/,""/; s/,"",/,/; s/ ,/,/' | \
	perl -p -e 's/\s*[UJ].{1,2}$$//; s/˂/</; s/<[0-9]..[0-9]*/0/' | \
	csvsql --query "select * from stdin where fixture_location not like '%Follow Up%' \
										  and fixture_location not like '%repair%' \
										  and fixture_location not like '%Test 2%' \
										  and fixture_location not in ('Indoor', 'Outdoor', 'Oudoor')"| \
	python scripts/pivot_park_headers.py > $@

output/parks_lead_scores.csv : clean_scrape.csv
	cat $< | python scripts/parks_score.py > $@

.PHONY : clean_parks
clean_parks :
	rm clean_scrape.csv
