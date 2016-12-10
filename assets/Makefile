PG_DB = water

water_projects : water_projects.geojson
	ogr2ogr -f PostgreSQL PG:"dbname=$(PG_DB)" -nln $@ $<
	psql -d $(PG_DB) -c "alter table water_projects alter column project_submit_date type timestamp using timestamp 'epoch' + project_submit_date * interval '1 millisecond'"
	psql -d $(PG_DB) -c "alter table water_projects alter column enddate type timestamp using timestamp 'epoch' + enddate * interval '1 millisecond'"
	psql -d $(PG_DB) -c "alter table water_projects alter column startdate type timestamp using timestamp 'epoch' + startdate * interval '1 millisecond'"

foia : chi-water-mains-work/WaterCIP2016_20161121.xlsx
	in2csv $< |\
	csvsql --db postgresql:///$(PG_DB) --table $@ --insert

2011_projects.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)" \
            -sql "SELECT * FROM water_projects WHERE startdate < '2012-01-01'::DATE AND (enddate IS NULL or enddate >= '2011-01-01'::DATE)"

2012_projects.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)" \
            -sql "SELECT * FROM water_projects WHERE startdate < '2013-01-01'::DATE AND (enddate IS NULL or enddate >= '2012-01-01'::DATE)"

2013_projects.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)" \
            -sql "SELECT * FROM water_projects WHERE startdate < '2014-01-01'::DATE AND (enddate IS NULL or enddate >= '2013-01-01'::DATE)"

2014_projects.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)" \
            -sql "SELECT * FROM water_projects WHERE startdate < '2015-01-01'::DATE AND (enddate IS NULL or enddate >= '2014-01-01'::DATE)"

2015_projects.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)" \
            -sql "SELECT * FROM water_projects WHERE startdate < '2016-01-01'::DATE AND (enddate IS NULL or enddate >= '2015-01-01'::DATE)"

2016_projects.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)" \
            -sql "SELECT * FROM water_projects WHERE startdate < '2017-01-01'::DATE AND (enddate IS NULL or enddate >= '2016-01-01'::DATE)"

all_years.geojson :
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)"

$(PG_DB) :
	createbd $@
	psql -d $@ -c "CREATE EXTENSION POSTGIS"

