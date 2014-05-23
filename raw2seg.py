import sys
import re

sepFile = file('space.txt')
space = sepFile.readline().strip().decode('utf-8')
sepFile.close()

sys.stderr.write('--------------------------------------------------------------\n')
sys.stderr.write('The scirpt convert raw xinhua files to segmented sentences,\n')
sys.stderr.write('the annotations and html style tags will be removed\n')
sys.stderr.write('--------------------------------------------------------------\n')
for num, line in enumerate(sys.stdin):
	if num > 0 and num % 10000 == 0:
		sys.stderr.write("processing %d line\r" %num)

	#sys.stderr.write(line)
	#print ("\n\nline: %d" %num) + line,
	items = re.split(space, line.strip().decode('utf-8'))

	#print items
	items = filter(lambda x: x != space, items)
	items = filter(lambda x: len(x) > 1 and not(x[0] == '<' and x[len(x) - 1] == '>'), items)
	
#	if len(items) > 0:
#		print ' '.join(items).encode('utf-8')
	# remove the annotation 
	# e.g. 
	#			xxx(vh11), (vh11) will be removed

	if len(items) > 0:
		for i, item in enumerate(items):
			if item.find('(', 1) >= 0:
				items[i] = item[:item.index('(', 1)]
			else:
				if items[i] != u'(FW)':
					sys.stderr.write('\n' + items[i].encode('utf-8') + '\n')
				items[i] = u''

		items = filter(lambda x: len(x) > 0, items)

		if len(items) > 0:
			print '<s> ' + ' '.join(items).encode('utf-8') # adding a start symbol

		
		



	
