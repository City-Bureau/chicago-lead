import sys
import csv

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

writer.writerow(next(reader))

park_name = None

for location, result in reader:
    if not result:
        park_name = location
    else:
        writer.writerow([park_name, location, result])
