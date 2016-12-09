PG_DB=cps-lead
CSV=school_lead_report_utf8.csv

.PHONY: clean
clean:
	rm -r lead_reports crosswalk
	psql -d $(PG_DB) -c "DROP TABLE lead_reports;"

lead_reports:
	csvsql --db postgresql:///$(PG_DB) --table $@ --insert $(CSV)
	touch $@

school_coordinates.csv: lead_reports
	python scripts/school_coordinates.py $(PG_DB) > $@ 

missing_school_coordinates.csv: school_coordinates.csv
	cat error.csv | scripts/error_coordinates.py > $@ 

geocoded_schools: school_coordinates.csv missing_school_coordinates.csv
	csvsql --db postgresql:///$(PG_DB) --table school_coordinates --insert school_coordinates.csv
	csvsql --db postgresql:///$(PG_DB) --table missing_school_coordinates --insert missing_school_coordinates.csv
	psql -d $(PG_DB) -c \
		"DELETE FROM school_coordinates WHERE long_name IS null;"
	psql -d $(PG_DB) -c \
		"SELECT x.* INTO $@ FROM (\
			(SELECT * FROM school_coordinates) \
			UNION \
			(SELECT * FROM missing_school_coordinates)\
				) AS x";
	touch $@

geocoded_schools.csv: geocoded_schools
	psql -d $(PG_DB() -c \
		"COPY geocoded_schools TO STDOUT DELIMITER ',' CSV HEADER;" > $@
