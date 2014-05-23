import sys, re

dict = {}

for line in sys.stdin:
	items = filter(lambda x: len(x) > 0, re.split('\s+', line))
	if (len(items) != 0):
		dict[items[0]] = True

print '\n'.join(['<s>', '</s>', '<unk>'])
for key in dict:
	if (len(key) == 0):
		sys.stderr.write(key, '-----------')
	print key