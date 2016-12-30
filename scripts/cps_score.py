import sys
import csv
import itertools

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

next(reader)
writer.writerow(['school_name', 'score', 'num_fixtures'])

for school_name, measurements in itertools.groupby(reader, lambda x: x[0]):
    fixture_scores = []
    school_name = school_name.title()
    for fixture, measurements in itertools.groupby(measurements, lambda x: '-'.join(x[1].split('-')[:-1])):
        fixture_measurements = list(measurements)
        num_trials = len(fixture_measurements)
        try:
            count = sum(float(result) > 15 for _, _, _, _, result, _ in fixture_measurements)
        except ValueError:
            continue
        score = count / num_trials
        fixture_scores.append(score)
    if not fixture_scores:
        writer.writerow([school_name, None, None])
        continue
    writer.writerow([school_name, sum(fixture_scores)/len(fixture_scores), len(fixture_scores)])