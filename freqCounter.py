import sys
import re
c = {}
total = 0
for i, line in enumerate(sys.stdin):
	if ((i + 1) % 100000 == 0):
		sys.stderr.write('%d line\r' %(i + 1))
	line = line.strip().decode('utf-8')

	items = re.split(u'\s+', line)
	total += len(items)
	for item in items:
		if item  not in c:
			c[item] = 1
		else:
			c[item] += 1

sortedList = sorted (c.items(), key = lambda x: x[1], reverse = True)

ratio = 0
for item in sortedList:
	ratio += 100.0 * item[1] / total
	sys.stdout.write('%-5s %-5d %.2f%%\n' %(item[0].encode('utf-8'), item[1], ratio))

