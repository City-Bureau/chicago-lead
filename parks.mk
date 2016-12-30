tabula = java -jar ./tabula-java/target/tabula-0.9.1-jar-with-dependencies.jar

tabula-java :
	git clone https://github.com/tabulapdf/tabula-java.git
	cd tabula-java && mvn clean compile assembly:single

.INTERMEDIATE : tabula/parks.csv
tabula/parks.csv : raw/Water_Fountain_Testing_Final_Results.pdf tabula-java
	$(tabula) -p all -g $< > $@

.INTERMEDIATE : park_fixtures.csv
park_fixtures.csv : tabula/parks.csv
	tail -n +7 $< | \
	perl -p -e 'print "fixture_location,result\n" if $$. == 1' | \
	perl -p -e 's/^("",)*//' | \
        perl -p -e 's/(,""){2}/,""/' | \
        perl -p -e 's/,"",/,/' | \
        perl -p -e 's/ ,/,/' | \
	perl -p -e 's/\s*[UJ].{1,2}$$//' | \
        perl -p -e 's/˂/</' | \
        csvgrep -c fixture_location -r ".*(Follow Up|repair|Test 2|Indoor|Outdoor|Oudoor).*" -i | \
	python scripts/pivot_park_headers.py > $@

output/parks_lead_scores.csv : park_fixtures.csv
	cat $< | python scripts/parks_score.py > $@

