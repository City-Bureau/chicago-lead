PG_DB = water

.PHONY : setupdb
setupdb : 
	make $(PG_DB)
	make water_projects

$(PG_DB) :
	createdb $@
	psql -d $@ -c "CREATE EXTENSION POSTGIS"

water_projects : raw/water_projects.geojson
	ogr2ogr -f PostgreSQL PG:"dbname=$(PG_DB)" -nln $@ $<
	psql -d $(PG_DB) -c "alter table water_projects alter column project_submit_date type bigint using (project_submit_date::bigint), \
	alter column enddate type bigint using (enddate::bigint), alter column startdate type bigint using (startdate::bigint)"
	psql -d $(PG_DB) -c "alter table water_projects alter column project_submit_date type timestamp using timestamp 'epoch' + project_submit_date * interval '1 millisecond'"
	psql -d $(PG_DB) -c "alter table water_projects alter column enddate type timestamp using timestamp 'epoch' + enddate * interval '1 millisecond'"
	psql -d $(PG_DB) -c "alter table water_projects alter column startdate type timestamp using timestamp 'epoch' + startdate * interval '1 millisecond'"

foia : raw/WaterCIP2016_20161121.xlsx
	in2csv $< |\
	csvsql --db postgresql:///$(PG_DB) --table $@ --insert

output/water_projects_all_years.geojson : setupdb
	ogr2ogr -f GeoJSON $@ "PG:dbname=$(PG_DB)"

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

.PHONY : clean_water_projects
clean_water_projects :
	dropdb $(PG_DB)