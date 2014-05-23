import sys
import re

buf = ''
for i,line in enumerate(sys.stdin):
	if i % 100000 == 0:
		sys.stderr.write("processing line %d\r" %i)
	
	if line[0] == '<':
		line = line.strip()
		if line[:2] == '</':
			if len(buf) > 0:
				sys.stdout.write(buf + '\n')
				buf = ''
	else:
		line = line.strip()
		buf += line + ' '
