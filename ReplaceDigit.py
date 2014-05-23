import sys
import re

pDigit =re.compile('(\d+\,)*\d+(\.\d*)*')
for i, line in enumerate(sys.stdin):
	if i % 100000 == 0:
		sys.stderr.write('processing line %d\r' %i)

	words = re.split('\s+', line.strip())
	for (i, word) in enumerate(words):
		words[i] = pDigit.sub('DIGIT', word)
	sys.stdout.write(' '.join(words) + '\n')

	
