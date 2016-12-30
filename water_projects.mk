raw/water_projects.geojson :
	esridump http://gisapps.cityofchicago.org/arcgis/rest/services/ExternalApps/CDOT_Resolution/MapServer/32 raw/water_projects.geojson


.INTERMEDIATE : older_water_projects.geojson
older_water_projects.geojson : raw/water_projects.geojson
	cat $< | python scripts/convert_timestamps.py > $@


raw/Sections\ to\ Trace\ -\ to_be_traced.csv : raw/WaterCIP2016_20161121.xlsx  
	# Hand Traced at
	# https://docs.google.com/spreadsheets/d/1XHXLWtJi4I2y5ARhBNzLLH_bH_gZhV0KnBFEqA0bEUM/edit#gid=257982765

.INTERMEDIATE : traces.geojson
traces.geojson : raw/Sections\ to\ Trace\ -\ to_be_traced.csv
	cat "$<" | python scripts/traces.py > $@

output/water_projects.geojson : older_water_projects.geojson traces.geojson
	python scripts/merge_geojson.py $^ > $@
