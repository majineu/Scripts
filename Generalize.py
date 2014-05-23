#!/usr/bin/env python
import sys
# in branch2
strDig = '1234567890' 
sys.stderr.write('convert digit and detect urls\n')
for i, line in enumerate(sys.stdin):
	if i % 10000 == 0:
		sys.stderr.write('processing %d line\r' %i)

	line = line.strip()
	words = line.split()
	if len(words) == 0:
		sys.stdout.write('\n')
		continue

	beg, chBeg = -1, -1
	newWord = ''

	word = words[0]
	if word.find('http://') == 0 or word.find('www.') == 0:
		newWord = 'url'
	else:
		for idx in range(0, len(word), 1):
			if word[idx] in strDig:
				if beg == -1:
					beg = idx
					newWord += '#dg'

			else:
				beg, chBeg = -1, -1
				newWord += word[idx]

	words.insert(1, newWord.lower())
	sys.stdout.write((' '.join(words)) + '\n')

			
				

