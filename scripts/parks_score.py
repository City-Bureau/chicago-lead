import sys
import csv
import itertools

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

next(reader)
writer.writerow(['park_name', 'score', 'num_fixtures'])

for park_name, measurements in itertools.groupby(reader, lambda x: x[0]):
    measurements = list(measurements)
    count = sum(float(result) > 15 for _, _, result in measurements)
    num_fixtures = len(measurements)
    score = count / num_fixtures
    writer.writerow([park_name, score, num_fixtures])
