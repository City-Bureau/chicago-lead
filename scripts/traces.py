import csv
import json
import sys

features = []

reader = csv.DictReader(sys.stdin)
for row in reader:
    json_string = row.pop('GeoJSON')

    if json_string:
        if 'FeatureCollection' not in json_string:
            json_string = '{"type" : "FeatureCollection", "features" : [' + json_string

        try:
            geometry = json.loads(json_string)
        except:
            import pdb
            pdb.set_trace()
        feature = {'type' : "Feature",
                   'properties' : row,
                   'geometry' : geometry['features'][0]['geometry']}
        features.append(feature)


geojson = {'type' : "FeatureCollection",
           'features' : features}

json.dump(geojson, sys.stdout)
