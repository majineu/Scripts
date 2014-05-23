import sys
import re  

items = []

for line in sys.stdin:
	if len(line.strip()) == 0:
		if len(items) != 0:
			rel = ''
			for item in items:
				if item.find('REL') != -1:
					rel += item.split()[0] + '_' + item.split()[2] + ' '
			if len(rel) > 0:
				sys.stdout.write(rel + '\n')

			items = []
	else:
		items += [line.strip()]
