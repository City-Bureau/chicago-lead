import csv
import sys

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

header = next(reader)
writer.writerow(header)

for line in reader:
    school, sample, location, date, result, pdf = line
    if (school in ['Collinshs', 'Tanner', 'Powell']) or (not result):
        continue
    if (school == 'Ogden') and ('610529' in pdf):
        school = 'Ogdenhs'
    if '-' not in sample:
        sample = location
    if (result in ['None Detected', 'ND']) or ('<' in result):
        result = 0
    writer.writerow([school, sample, location, date, result, pdf])
