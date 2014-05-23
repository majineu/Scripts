#!/usr/bin/env python
import sys
import re


# read entity indexes
if len(sys.argv) != 3:
	sys.stderr.write('usage: xx.py < input entityIndexFile lenCutoff > output')
	exit(0)

indexes = []
fIndex = file(sys.argv[1])
for line in fIndex:
	line = line.strip()
	indexes += [re.split('\s+', line.strip())]
fIndex.close()

cutoff = int(sys.argv[2])

tokens, senNum = [], 0
sys.stdout.write('Entity1\tRelation\tEntity2\n')
for line in sys.stdin:
	line = line.strip()
	if len(line) == 0:
		if len(tokens) == 0:
			continue
		
		rel = ''		# denote there is no relation
		for token in tokens:
			if token.find('REL') != -1:
				rel += re.split('\s+', token)[0] + ' '

		if len(rel) == 0:
			rel = '---'


		enIdx = indexes[senNum]
	
		# updated, support length cutoff
		# length: words between the two entites
		if int(enIdx[2]) - int(enIdx[1]) >= cutoff:
			rel = '---'
		
		senNum += 1

		# write entity 1
		sys.stdout.write(re.split('\s+', tokens[int(enIdx[0])])[0])
		for i in range(int(enIdx[0]) + 1, int(enIdx[1]), 1):
			sys.stdout.write(' ' + re.split('\s+', tokens[i])[0])
		sys.stdout.write('\t')
		
		# write relation
		sys.stdout.write(rel + '\t')
		
		# write entity 2
		sys.stdout.write(re.split('\s+', tokens[int(enIdx[2])])[0])
		for i in range(int(enIdx[2]) + 1, int(enIdx[3]), 1):
			sys.stdout.write(' ' + re.split('\s+', tokens[i])[0])
		sys.stdout.write('\n')

		tokens = []
	else:
		tokens += [line]


