import csv
import sys

import googlemaps

# addto a file called secrets.py:
#     * USER = <your postgres username>
#     * GOOGLE_KEY = <your google maps api key>
import secrets

gmaps = googlemaps.Client(key=secrets.PLACES_KEY)

writer = csv.writer(sys.stdout)
reader = csv.reader(sys.stdin)

header = ['school', 'long_name', 'latitude', 'longitude']
writer.writerow(header)

for record in reader:
    try:
        school = record[0]
        result = gmaps.places(school + ' School Chicago IL')
        result = result['results'][0]
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        long_name = result['name']
        out = [school, long_name, lat, lng]
        writer.writerow(out)
    except TypeError:
        pass
    except IndexError:
        school = record[0][0]
        out = [school, '', '', '']
        writer.writerow(out)
