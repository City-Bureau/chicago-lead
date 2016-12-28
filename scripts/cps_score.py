import csv
import itertools
import sys

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

next(reader)
writer.writerow(['school_name', 'score', 'num_fixtures'])

for school_name, measurements in itertools.groupby(reader, lambda x: x[0]):
	fixture_scores = []
	for fixture, measurements in itertools.groupby(measurements, lambda x: '-'.join(x[1].split('-')[:-1])):
		m = list(measurements)
		num_trials = len(m)
		count = sum(float(result) > 15 for _, _, _, _, result, _ in m)
		score = count / num_trials
		fixture_scores.append(score)
	writer.writerow([school_name, sum(fixture_scores)/len(fixture_scores), len(fixture_scores)])