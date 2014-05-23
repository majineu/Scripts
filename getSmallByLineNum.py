import sys
import re

if len(sys.argv) != 3:
	sys.stderr.write('usage: xx.py reslineNum  input > output')
	exit(0)

resLineNum = int(sys.argv[1])
lineNum = sum(1 for line in file(sys.argv[2]))
step = lineNum / resLineNum
lineWrite = 0
for i, line in enumerate(file(sys.argv[2])):
	if i % 500000 == 0 and i != 0:
		sys.stderr.write('processing %d line\r' %i)
	
	if i % step == 0 and i != 0:
		print line,
		lineWrite += 1
		if lineWrite == resLineNum:
			break

