import sys
import csv
import itertools

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

def above_threshold(result):
    if '<' in result:
        return False
    elif 'None Detected' in result:
        return False
    elif result == '':
        return float('nan')
    else:
        try:
            return float(result) > 15
        except:
            print('foo', result)
            raise
    

next(reader)

writer.writerow(['school_name', 'score', 'num_fixtures', 'filename'])

for school, measurements in itertools.groupby(reader, lambda x: x[0]):
    fixture_scores = []
    for fixture, measurements in itertools.groupby(measurements, lambda x: '-'.join(x[1].split('-')[:-1])):
        fixture_measurements = [each for each in measurements if each != '']
        num_trials = len(fixture_measurements)
        count = sum(above_threshold(result)
                    for _, _, _, _, result, _ in fixture_measurements)
        score = count / num_trials
        fixture_scores.append(score)

    writer.writerow([school.title(),
                     sum(fixture_scores)/len(fixture_scores),
                     len(fixture_scores),
                     fixture_measurements[-1][-1]])
