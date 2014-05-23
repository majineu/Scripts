import sys
import re

if __name__ == '__main__':
	items = []
	thres = float(sys.argv[1])
	for line in sys.stdin:
		if line.find('-----') != -1:
			#sys.stdout.write('items:' + '\n'.join(items) + '\n\n')
			if len(items) > 0 and float(items[10]) > thres:
				sys.stdout.write('\n'.join(items) + '\n\n')
			
			items = []
		else:
			items += [line.strip()]
