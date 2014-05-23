import sys
import re

ratio = int(sys.argv[1])

for i, line in enumerate(sys.stdin):
	if i % 500000 == 0:
		sys.stderr.write('processing %d line\r' %i)

	if i % ratio == 0:
		print line,
