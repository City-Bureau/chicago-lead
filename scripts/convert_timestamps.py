import sys
import json
import datetime

def convert(milliseconds_timestamp):
    if milliseconds_timestamp is not None:
        return str(datetime.datetime.fromtimestamp(milliseconds_timestamp / 1000))
    else:
        return None

geojson = json.load(sys.stdin)

for feature in geojson['features']:
    feature['properties']['PROJECT_SUBMIT_DATE'] = convert(feature['properties']['PROJECT_SUBMIT_DATE'])
    feature['properties']['STARTDATE'] = convert(feature['properties']['STARTDATE'])
    feature['properties']['ENDDATE'] = convert(feature['properties']['ENDDATE'])

json.dump(geojson, sys.stdout)

