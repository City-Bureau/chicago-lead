output/parks_lead_scores.csv: tabula-Water_Fountain_Testing_Final_Results.csv
	python scripts/clean_parks.py $< | python scripts/score_parks.py > $@
