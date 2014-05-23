import sys
import re
puncs = [",", ".", ":", "``", "''", "-LRB-", "-RRB-", "PU"]

nTotal, nPunc = 0, 0
for line in sys.stdin:
	if len(line.strip()) != 0:
		tokens = re.split('\s+', line.strip())
		if tokens[1] in puncs:
			nPunc += 1
#			print line
		nTotal += 1


print 'total %d, punc %d, rate %.2f' %(nTotal, nPunc, 100.0 * nPunc/nTotal)

