import sys
ntotal = 0
for line in sys.stdin:
	words = line.strip().split()
	for i in range(0, len(words), 1):
		if words[i].find('http://') == 0 or words[i].find('www.') == 0:
			sys.stderr.write(words[i] + '\n\n')
			words[i] = 'URL'
			ntotal += 1
	
	sys.stdout.write(' '.join(words) + '\n')
sys.stderr.write('total %d url converted\n'%ntotal)
