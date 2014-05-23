import sys
import re

sys.stderr.write('--------------------------------------------------------------\n')
sys.stderr.write('The convert segmented sentences to Chinese characters,\n')
sys.stderr.write('each characters are separated by space\n')
sys.stderr.write('--------------------------------------------------------------\n')

for num, line in enumerate(sys.stdin):
	if num > 0 and num % 10000 == 0:
		sys.stderr.write("processing %d line\r" %num)

	sent = line.strip().decode('utf8')
	sentNoSeg = filter(lambda x: x != ' ', sent)
	
	
	if len(sentNoSeg) > 1: 			#ignore sentences with only one char
		chars = map(lambda x: x + ' ', sentNoSeg)
		print '<s> ' +  ''.join(chars).encode('utf-8')  # adding a start symbol
