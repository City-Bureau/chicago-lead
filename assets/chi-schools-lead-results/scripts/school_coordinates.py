import csv
import sys

import psycopg2
import googlemaps

# addto a file called secrets.py:
#     * USER = <your postgres username>
#     * GOOGLE_KEY = <your google maps api key>
import secrets

PG_DB = sys.argv[1]
USER = secrets.USER

conn = psycopg2.connect(
    database=PG_DB,
    user=USER
)

cur = conn.cursor()

cur.execute("SELECT DISTINCT school from lead_reports;")

gmaps = googlemaps.Client(key=secrets.GOOGLE_KEY)

writer = csv.writer(sys.stdout)

header = ['school', 'long_name', 'latitude', 'longitude']
writer.writerow(header)

missed_schools = []

for record in cur:
    try:
        school = record[0]
        result = gmaps.geocode(school + ' School Chicago IL')
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']
        long_name = result[0]['address_components'][0]['long_name']
        out = [school, long_name, lat, lng]
        writer.writerow(out)
    except TypeError:
        pass
    except IndexError:
        school = record[0]
        out = [school, '', '', '']
        writer.writerow(out)
        missed_schools.append(school)

with open('error.csv', 'w') as err:
    err_writer = csv.writer(err)
    for school in missed_schools:
        err_writer.writerow([school])

cur.close()
conn.close()
