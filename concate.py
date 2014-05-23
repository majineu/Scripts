import sys
import re

conPunc = {}
puncFile = file('concate_punc.txt')

for line in puncFile:
	punc = line.strip().decode('utf-8')
	conPunc[punc] = 1

puncFile.close()


sys.stderr.write('--------------------------------------------------------------\n')
sys.stderr.write('The script combine lines end up with , ; with \n')
sys.stderr.write('the following line to make it longer\n')
sys.stderr.write('--------------------------------------------------------------\n')

lineCache = u""
for i, line in enumerate(sys.stdin):
	
	if i % 100000 == 0:
		sys.stderr.write('processing %d lines\r' %i)

	line = line.strip().decode('utf-8')
	
	if len(line) < 1:
		sys.stderr.write('\nline %d: empty\n' %i)
		
		if len(lineCache) > 1:
			print lineCache.encode('utf-8')
		
		continue

	
	if line[len(line) - 1] in conPunc:
		lineCache += line + u' '
	else:
		if len(lineCache + line) > 0:
			try:
				print (u'<s> ' + lineCache + line).encode('utf-8')    # here we add a start symbol
			except:
				sys.stderr.write('\nline %d encoding failed\n')
				pass
		lineCache = u''

	

