import sys
import re


quot = 0
allUpper = 0
sen = []
totalUpper = 0


def toLower(seq = []):
	sys.stderr.write('\n----------------------\n' + '\n'.join(seq) + '\n\n')
	for idx, item in enumerate(seq):
		words = item.split()
		words[0] = words[0].lower()
		seq[idx] = ' '.join(words)
	sys.stderr.write('\n'.join(seq) + '\n\n-----------------------\n')

for i, line in enumerate(sys.stdin):
	words = line.strip().split()
	if len(words) == 0:
		if allUpper == 1:
			toLower(sen)
			totalUpper += len(sen) 
		sys.stdout.write('\n'.join(sen) + '\n\n')
		quot = 0
		allUpper = 1
		sen = []
		continue

	if words[0].isalpha():
		if words[0].isupper() == False:
			allUpper = 0
		elif len(words[0]) > 4:
			words[0] = words[0].lower()
	
	else:
	
		if words[0] == '"' or words[0] == '\'':
			if quot == 1:
				words[0], words[1] = '\'\'', '\'\''
				quot = 0
			else:
				words[0], words[1] =  '``', '``'
				quot = 1
		
		elif words[0] in ['(', '[', '<', '{', '<<']:
			words[0], words[1] = '-LRB-', '-lrb-'
		elif words[0] in ['(', ']', '>', '}', '>>']:
			words[0], words[1] = '-RRB-', '-rrb-'
		elif  words[0].find('.com') != -1 or words[0].find('.org') != -1 or words[0].find('.gov') != -1 or words[0].find('.htm') != -1:
			words[0], words[1] = 'url', 'url'

	
	item = ' '.join(words)
	sen += [item]

sys.stderr.write('total upper sen converted %d\n' %totalUpper)
