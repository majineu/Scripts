import re
import sys

sen = []
words, pos, labels, ids = [], [], [], []
for i, line in enumerate(sys.stdin):
	line = line.strip()
	if i % 5 == 0:
		words = re.split('\s+', line)
	elif i % 5 == 1:
		pos = re.split('\s+', line)
	elif i % 5 == 2:
		labels = re.split('\s+', line)
	elif i % 5 == 3:
		ids = re.split('\s+', line)
	elif i % 5 == 4:
		for i in range(0, len(words), 1):
			sys.stdout.write('%s %s %s %s\n' %(words[i], pos[i], ids[i], labels[i]))
		sys.stdout.write('\n')
