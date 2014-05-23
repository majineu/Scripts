from TreeClass import *

if (len(sys.argv) not in [4, 5, 6]):
	sys.stderr.write('usage: python  GetSen.py  [row|col]  inputFile  outputFile  (tag)  (conll)\n')
	sys.stderr.write('  row: each line is a sentence, the default value\n')
	sys.stderr.write('  col: each line is a word\n')
	sys.stderr.write(' note: input and output file are all in utf-8 format')
	sys.exit(0)


fIn  = file(sys.argv[2])
fOut = file(sys.argv[3], 'w')

sentence = []
for i, line in enumerate(fIn):
	
	if (i != 0 and i % 10000 == 0):
		sys.stderr.write('%d\r' %i)

	items = filter(lambda x: len(x) > 0, re.split('\s+', line.decode('utf-8')))
	
	if (len(items) == 0):

		if (len(sentence) != 0):
			if (sys.argv[1] == 'row'):
				fOut.write(u'\t'.join(sentence).encode('utf-8') + '\n')
			else:
				fOut.write(u'\n'.join(sentence).encode('utf-8') + '\n\n')
			sentence = []
	else:

		word, tag = '', ''
		if ('conll' in sys.argv):
			word, tag = items[1], items[3]
		else:
			word, tag = items[0], items[1]


		if ('tag' in sys.argv):
			sentence += [word + u'\t' + tag]
		else:
			sentence += [word]

