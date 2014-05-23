import sys
import re

if __name__ == '__main__':

	if len(sys.argv) != 3:
		sys.stderr.write('usage: xx.py < ground-truth  output  idxFile\n')
		sys.stderr.write('extract entity and relation from ground-truth file\n')
		exit(0)

	fOut = open(sys.argv[1], 'w')
	fIdx = open(sys.argv[2], 'w')
	for i, line in enumerate(sys.stdin):
		if i == 0:
			continue

		line = line.strip()
		if len(line) > 0:
			
			# the case that neither O-CRF nor our system could handle
			if line.rfind('}}}') > line.rfind(']]]'):
				fOut.write('ASIA --- ASIA\n')
				fIdx.write('0 1   2 3\n')
			else:
				items = re.split('\t', line)
				en1, en2 = items[0], items[2]
				rel, sen  = items[1], items[4]

				en1_tokens = en1.split()
				en2_tokens = en2.split()
				
				# write the first entity
				fOut.write(en1 + ' ')
				fIdx.write('0 %d   ' %len(en1_tokens))
	
				# processing relation
				innerWords = sen[sen.find(']]]') + 4: sen.rfind('[[[')].split()
				en2idx = len(en1_tokens)
				
				if rel == '---':
					fOut.write(' '.join(innerWords) + ' ')
					en2idx += len(innerWords)
				else:
					for idx in range(0, len(innerWords), 1):
						if innerWords[idx] not in ['--->', '<---']:
							if innerWords[idx].find('{{{') != -1:
								innerWords[idx] = innerWords[idx][3:-3] 
							fOut.write(innerWords[idx] + ' ')
							en2idx += 1
	
				# write the second entity
				fOut.write(en2 + '\n')
				fIdx.write('%d %d\n' %(en2idx, en2idx + len(en2_tokens)))
				en2idx += len(innerWords)

	fIdx.close()
	fOut.close()


			


