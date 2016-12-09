### CPS Lead Report Data

## Requirements

* GNU Make (built in on OS X and Linux)
* PostgreSQL 
* psycopg2 (`pip install psycopg2`)
* googlemaps (`pip install googlemaps`)

Also requires Google Maps API keys for geocoding school locations. [Sign into the developer console with your google account to create a key.](https://developers.google.com/maps/documentation/geocoding/start). You'll need to enable keys for both the Places API and the Geocoding API (the APIs cover each other's holes).

## Make the data

Start by creating a database:

```bash
createdb cps-lead
```

Then set up your secret variables in `scripts/secrets.py` for building the geocoded crosswalk:

```python
USER = "<your postgres username>"
GEOCODING_KEY = "<your geocoding API key>" 
PLACES_KEY = "<your places API key>"
```

Then geocode the schools:

```bash
make geocoded_schools
```

If you just want a CSV file, you can run `make geocoded_schools.csv`.