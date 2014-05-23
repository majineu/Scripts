import re
import sys

sen = []
n = 0
for line in sys.stdin:
	if len(line.strip()) == 0:
		if len(sen) > 0:
			n+= 1
			words, pos = [], []
			hids, labels = [], []
			for line in sen:
				tokens = re.split('\s+', line)
				words += [tokens[0]]
				pos   += [tokens[1]]
				hids  += [tokens[2]]
				labels+= [tokens[3]]

			print '\t'.join(words)
			print '\t'.join(pos)
			print '\t'.join(labels)
			print '\t'.join(hids)
			sys.stdout.write('\n')
		sen = []
	else:
		sen += [line.strip()]

#if len(sen) > 0:
#	words, pos = [], []
#	hids, labels = [], []
#	n += 1
#	for line in sen:
#		tokens = re.split('\s+', line)
#		words += [tokens[0]]
#		pos   += [tokens[1]]
#		hids  += [tokens[2]]
#		labels+= [tokens[3]]
#
#		print '\t'.join(words)
#		print '\t'.join(pos)
#		print '\t'.join(labels)
#		print '\t'.join(hids)
#		sys.stdout.write('\n')
#
sys.stderr.write('total %d sen\n' %n)
