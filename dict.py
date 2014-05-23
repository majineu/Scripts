import sys
import re

wDict = {}
for line in sys.stdin:
	line = line.strip().decode('utf-8')
	words = re.split(u' ', line)
#	sys.stderr.write('number of words %d\n' % len(words))
	for word in words:
#		sys.stderr.write('word %s:\n'%word.encode('utf-8'))
		wDict[word] = 0

sys.stderr.write('total number of words %d\n' %len(wDict))
wDict[u'</s>'] = 0
wDict[u'NULL'] = 0
id = 0
for word in wDict.keys():
	id += 1
	if id % 100 == 0:
		sys.stderr.write('%d %s\n'%(id, word.encode('utf-8')))

fTrain = file('../JointPOS/train.classify', 'r')
for line in fTrain:
	line = line.strip().decode('utf-8')
	words = re.split(' ', line)
	for word in words[:-1]:
		if word not in wDict:
			sys.stderr.write('unk %s\n'%word)

fTrain.close()
