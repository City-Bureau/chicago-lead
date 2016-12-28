PG_DB = parks_lead

$(PG_DB) : 
	createdb $(PG_DB)

clean_scrape.csv : tabula/tabula-Water_Fountain_Testing_Final_Results.csv
	sed -e '1s/^/fixture_location,result=/' $< | tr '=' '\n' | \
	sed -e 's/^\("",\)*//' -e 's/\(,""\)\{2,\}/,""/' -e 's/,"",/,/' -e 's/ ,/,/' | \
	sed -e 's/[0-9] *[UJ]//' -e 's/[<˂][0-9?.0-9]*/0/' | \
	csvsql --query "select * from stdin where fixture_location not like '%Follow Up%' \
										  and fixture_location not like '%repair%' \
										  and fixture_location not like '%Test 2%' \
										  and fixture_location not in ('Indoor', 'Outdoor', 'Oudoor')" | \
	python scripts/pivot_park_headers.py > $@

parks_lead_scores.csv : clean_scrape.csv $(PG_DB)
	csvsql --db postgresql:///$(PG_DB) --insert --table "lead_scores" --blanks $<
	psql -d $(PG_DB) -c "alter table lead_scores add exceeds_epa int"
	psql -d $(PG_DB) -c "update lead_scores set exceeds_epa = case when result <= 15 then 0 else 1 end;"
	psql -d $(PG_DB) -c "\copy (select park_name, count(*) as num_fixtures, round(avg(exceeds_epa), 4) as score from lead_scores group by park_name order by park_name) to 'output/$@' csv header"

.PHONY : clean_parks
clean_parks :
	rm clean_scrape.csv
	dropdb $(PG_DB)