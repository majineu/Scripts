from Tree import *
from ErrorDector import *

def PrintTopLevelTerminals(inPath = '', outPath = ''):
	fin		= file(inPath)
	fout	= file(outPath, 'w')
	foutTag		= file(outPath + '.headTag', 'w')
	foutWord	= file(outPath + '.headWord', 'w')
	
	(hTDict, hWDict) = ({}, {})
	
	for i, line in enumerate(fin):
		if i != 0 and i % 2000 == 0:
			sys.stderr.write('%d\r' %i)
		
		tree = CTree.BuildTree(line.strip().decode('utf-8'))
		level1Nodes = tree.GetNodeAtDepth(2)
		level1Nodes = filter(lambda x:x.IsPreterminal(), level1Nodes)
		wordList  = map(lambda x:x.GetChildren()[0].GetVal() + u'_' + x.GetVal(), level1Nodes)

		fout.write(str(i + 1) + u'\t'.join(wordList).encode('utf-8') + '\n')

		for wordTag in wordList:
			if wordTag.lower().find('head') != -1:
				(word, tag) = (wordTag.split(u'_')[0], wordTag.split(u'_')[1].split(u'##')[1])

				if word in hWDict:
					hWDict[word] += 1
				else:
					hWDict[word] = 1

				if tag in hTDict:
					hTDict[tag] += 1
				else:
					hTDict[tag] = 1


	
	sortWordList = sorted(hWDict.items(), key = lambda x: x[1], reverse = True)
	acc = 0
	for (word,count) in sortWordList:
		foutWord.write((word + u'\t\t:\t' + unicode(count) + '\t\t' + unicode(count + acc) + u'\n').encode('utf-8'))
		acc += count
	
	acc = 0	
	sortTagList = sorted(hTDict.items(), key = lambda x: x[1], reverse = True)
	for (tag,count) in sortTagList:
		foutTag.write((tag + u'\t\t:\t' + unicode(count) + '\t\t' + unicode(count + acc) + u'\n').encode('utf-8'))
		acc += count
	
	fin.close()
	fout.close()
	foutTag.close()
	foutWord.close()


#-------------------------------------------------------------------------------------
def headFindingRecall(goldPath, guessPath, resPath):
	fGold	= file(goldPath)
	fGuess	= file(guessPath)
	fRes	= file(resPath, 'w')
	(nCorrect, nTotal)= (0, 0)
	findStr = ['miss', 'find']
	nShort  = 0
	for nTotal, linePair in enumerate(zip(fGold, fGuess)):
		if  nTotal != 0 and nTotal % 1000 == 0:
			sys.stderr.write('processing line %d\r' %nTotal)

		goldTree	= CTree.BuildTree(linePair[0].strip().decode('utf-8'))
		guessTree	= CTree.BuildTree(linePair[1].strip().decode('utf-8'))

		# find head index
		goldPreTerminals	= goldTree.GetPreTerminals()
		if len(goldPreTerminals) < 6:
			nShort += 1
			continue

		headIndex = -1
		for (i,terminal) in enumerate(goldPreTerminals):
			if terminal.GetVal().lower().find(u'head') != -1:
				headIndex = i
				break

		if headIndex == -1:
			fRes.write('sentence %d no head\n\n' %nTotal)
			continue

		# find guess level 2 indexes
		(index, level2Nodes) =(0, guessTree.GetNodeAtDepth(2))
		level2Index = []
		for node in level2Nodes:
			if node.IsPreterminal() == True:
				level2Index += [index]
				index += 1
			else:
				index += len(node.GetTerminals())

		
		hit = headIndex in level2Index
		nCorrect += hit

		# find word list
		level2Nodes = filter(lambda x:x.IsPreterminal(), level2Nodes)
		wordList  = map(lambda x:x.GetChildren()[0].GetVal() + u'_' + x.GetVal(), level2Nodes)

		fRes.write('sentence: ' + str(nTotal + 1) + '\t' + findStr[hit] + '\n')
		fRes.write('gold: head %s\n' %(goldPreTerminals[headIndex].GetChildren()[0].GetVal() + u'_' + goldPreTerminals[headIndex].GetVal()).encode('utf-8'))
		fRes.write('guess: %s\n\n' %(u' '.join(wordList)).encode('utf-8'))
		if hit == False:
			goldTree.DisTreeStructure(fRes, 'utf-8')
			fRes.write('\n')
			guessTree.DisTreeStructure(fRes, 'utf-8')
			fRes.write('\n')
			

	nTotal -= nShort
	fRes.write('nCorrect: %d  nTotal: %d  recall: %.2f%%\n' %(nCorrect, nTotal, 100.0*nCorrect/nTotal))
	fRes.write('nShort: %d\n' %nShort)
	fRes.close()
	fGold.close()
	fGuess.close()



def usage():
	sys.stderr.write('python sigHanAnalysis.py  goldFile  testFile  compareResult\n')
	sys.stderr.write('python sigHanAnalysis.py  scores  trainFile goldFile  testFile  compareResult [toCoarseType]\n')


if __name__ == '__main__':
	#PrintTopLevelTerminals('sigHan\\headOnly.train.ctbTrees', 'sigHan\\topLevelWords.txt')
	#headFindingRecall('sigHan\\test.gold.withHead.txt', 'sigHan\\noHead_noSent.h2f.gr4', 'sigHan\\recall.gr4.txt')
	if len(sys.argv) not in [4, 6, 7]:
		usage()
		sys.exit(0)		
	
	#CErrorDector.ComparePOS(sys.argv[1], sys.argv[2], sys.argv[3])
	if len(sys.argv) == 4:
		CErrorDector.DetectSpanErrors(sys.argv[1], sys.argv[2], sys.argv[3])
	elif len(sys.argv) == 7:
		CErrorDector.Scoring(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
	else:
		CErrorDector.Scoring(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

	#CErrorDector.ComparePOS('sigHan\\test\\test.gold', 'sigHan\\result\\noHead_noSent.h2f.gr4', 'sigHan\\analysis\\pos.h2f.gr4')



