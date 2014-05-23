import sys
import re

hID = 0
for line in sys.stdin:
	line = line.strip()
	if len(line) == 0:
		sys.stdout.write('\n')
		hID = 0
	else:
		tokens = re.split('\s+', line)
		sys.stdout.write('%-10s %-10s %-3d NMOD\n' %(tokens[0], tokens[2], hID))
		hID += 1
