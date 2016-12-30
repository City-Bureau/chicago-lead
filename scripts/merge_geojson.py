import sys
import json

with open(sys.argv.pop(1)) as f:
    geojson = json.load(f)

for file_name in sys.argv[1:]:
    with open(file_name) as f:
        geojson['features'].extend(json.load(f)['features'])

json.dump(geojson, sys.stdout)

                                   
