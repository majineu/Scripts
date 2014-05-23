#!/usr/bin/env python
import re
import sys

def WriteToken(token, phraseType, isBeg):
	word = token[:token.find('_')]
	pos  = token[token.find('_') + 1:]
	chk  = 'I-' + phraseType
	if isBeg:
		isBeg = False
		chk = 'B-' + phraseType
	
	if phraseType == 'O':
		chk = 'O'
	sys.stdout.write('%-10s %-10s %-10s %-10s null\n' %(word, word.lower(), pos, chk))

sys.stderr.write('Converting chunked file to crf format...\n')
for line in sys.stdin:
	line = line.strip()
	if len(line) > 0:
		tokens = re.split('\s+', line);
		i = 0
		
		while i < len(tokens):
			if tokens[i][0] == '[':
				phraseType = tokens[i][1:]
				i += 1
				isBeg = True
				
				while tokens[i][-1] != ']':
					WriteToken(tokens[i], phraseType, isBeg)
					isBeg = False
					i += 1

				if len(tokens[i]) > 1:
					WriteToken(tokens[i][:-1], phraseType, isBeg)
				i+=1
			else:
				WriteToken(tokens[i], 'O', False)
				i += 1		
		sys.stdout.write('\n')

sys.stderr.write('Done\n')

