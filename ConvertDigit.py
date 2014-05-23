import sys

fDigit = file('digit.txt')
strDig 	 	= fDigit.readline()
strChDig 	= fDigit.readline()

strDig 		= strDig.strip().decode('utf-8')
strChDig 	= strChDig.strip().decode('utf-8')
fDigit.close()

for i, line in enumerate(sys.stdin):
	if i % 10000 == 0:
		sys.stderr.write('processing %d line\r' %i)

	line = line.strip().decode('utf-8')
	words = line.split()

	for i, word in enumerate(words):
		beg, chBeg = -1, -1
		newWord = u''

		for idx in range(0, len(word), 1):
			if word[idx] in strDig:
				if beg == -1:
					beg = idx
					newWord += u'DIG'

			elif word[idx] in strChDig:
				if chBeg == -1:
					chBeg = idx
					newWord += u'dig'

			else:
				beg, chBeg = -1, -1
				newWord += word[idx]

		words[i] = newWord;
	sys.stdout.write((u' '.join(words)).encode('utf-8') + '\n')

			
				

