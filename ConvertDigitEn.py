import sys

fDigit = file('digitEn.txt')
strDig = fDigit.readline()
trDig = strDig.strip()
fDigit.close()

for i, line in enumerate(sys.stdin):
	if i % 10000 == 0:
		sys.stderr.write('processing %d line\r' %i)

	line = line.strip()
	words = line.split()

	for i, word in enumerate(words):
		beg, chBeg = -1, -1
		newWord = ''

		for idx in range(0, len(word), 1):
			if word[idx] in strDig:
				if beg == -1:
					beg = idx
					newWord += '#DG'

			else:
				beg, chBeg = -1, -1
				newWord += word[idx]

		words[i] = newWord;
	sys.stdout.write((' '.join(words)) + '\n')

			
				

