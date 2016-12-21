import sys

name = 'park_name'
lines = []

for line in sys.stdin.readlines():
	if ',\n' in line:
		name = line.rstrip(',\n')
	line = '%s,%s' % (name,line)
	lines.append(line)

lines.append(lines.pop(-1).rstrip('\n'))

print(''.join([line for line in lines if ',\n' not in line]))