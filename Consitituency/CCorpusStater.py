from Tree import *

class CCorpusStater(object):
	"""description of class"""
	
	@staticmethod
	def StatWordPerTree(tree = CTree(), wCounter = {}):
		wts = tree.GetTagWordList()
		for node in wts:
			if node[0] in wCounter:
				wCounter[node[0]] += 1
			else:
				wCounter[node[0]] = 1


		

	@staticmethod
	def StatWordInfo(path,  outPath):
		
		fIn = file(path)
		fOut = file(outPath, 'w')
		(totalCount, tagCounter, wordCounter, tagWordCounter) = (0, {}, {}, {})
		for (i, line) in enumerate(fIn):
			if i != 0 and i % 5000 == 0:
				sys.stderr.write('processing line %d\r' %i)
			
			tree = CTree.BuildTree(line.strip().decode('utf-8'))
			tree = tree.RemoveOuterBr()
			if tree == None:
				continue

			wordTagList = tree.GetTagWordList()
			for (word, tag) in wordTagList:
				if word in wordCounter:
					wordCounter[word] += 1
				else:
					wordCounter[word] = 1

				if tag in tagCounter:
					tagCounter[tag] += 1
					tagWordCounter[tag][word] = 1
				else:
					tagCounter[tag] = 1
					tagWordCounter[tag] = {word:1}


			totalCount += len(wordTagList)


		sortedWord = sorted(wordCounter.items(), key = lambda x:x[1], reverse = True)
		sortedTag  = sorted(tagCounter.items(), key = lambda x:x[1], reverse = True)

		for item in sortedWord:
			fOut.write((item[0] + '\t\t:\t' + unicode(item[1])+ '\t' + unicode(100.0 * item[1]/totalCount) + u'\n').encode('utf-8'))
			
		fOut.write('\n\n--------------------------------------------\n')
		
		
		for item in sortedTag:
			fOut.write((item[0] + '\t\t:\t' + unicode(item[1]) + '\t' + unicode(100.0 * item[1]/totalCount) + u'\n').encode('utf-8'))
			
			for k, word in enumerate(tagWordCounter[item[0]]):
				if k % 50 == 0 and k != 0:
					break				
				fOut.write(word.encode('utf-8') + '\t')
			fOut.write('\n\n')
					

		fOut.write('\n\n--------------------------------------------\n')
		fOut.write('tag type %d, word type %d, total %d\n' %(len(sortedTag), len(sortedWord), totalCount))
		fOut.write('Average tag %.2f, Averge word %.2f\n' %(1.0*totalCount/len(sortedTag), 1.0*totalCount/len(sortedWord)))
		fOut.write('Average Length %.2f\n' %(1.0*totalCount/i))


		fOut.close()
		fIn.close()

	@staticmethod
	def StatNonterminals(path = '', outPath = ''):
		fIn = file(path)
		fOut = file(outPath, 'w')
		fOutTrees = file(outPath + '.trees', 'w')
		(non_terminalCounter, tagCounter, commons) = ({}, {}, {})
		for (i, line) in enumerate(fIn):
			if i != 0 and i % 5000 == 0:
				sys.stderr.write('processing line %d\r' %i)
			
			tree = CTree.BuildTree(line.strip().decode('utf-8'))
			tree = tree.RemoveOuterBr()

			nodeList = tree.GetPreOrderTreeList()
			for node in nodeList:
				if node.IsNonTerminal():
					label = node.GetVal().split(u'-')[0]
					if label in non_terminalCounter:
						non_terminalCounter[label] += [node]
					else:
						non_terminalCounter[label] = [node]

				elif node.IsPreterminal():
					if node.GetVal() in tagCounter:
						tagCounter[node.GetVal()] += [node]
					else:
						tagCounter[node.GetVal()] = [node]

		for key in tagCounter.keys():
			if key in non_terminalCounter:
				if key in commons:
					commons[key] += [node]
				else:
					commons[key] = [node]


		fOut.write('non-terminals :\n')
		sortedNTs = sorted(non_terminalCounter.items(), key = lambda x:x[0]) 
		for item in sortedNTs:
			fOut.write(('%s\t:%d\n' %(item[0], len(item[1]))).encode('utf-8'))
		
		fOut.write('\n\npre-terminals :\n')
		sortedPTs = sorted(tagCounter.items(), key = lambda x:x[0]) 
		for item in sortedPTs:
			fOut.write(('%s\t:%d\n' %(item[0], len(item[1]))).encode('utf-8'))

		fOut.write('\n\nintersection :\n')
		for item in commons.items():
			fOut.write(('%s\t:%d\n' %(item[0], len(item[1]))).encode('utf-8'))
		

		# write non-terminal related trees
		fOutTrees.write('non-terminals :\n')
		for item in non_terminalCounter.items():
			for i, tree in enumerate(item[1]):
				tree.DisTreeStructure(fOutTrees, 'utf-8')
				if i == 2: break
			
		
		fOutTrees.write('\n\n\n\n\n\npre-terminals :\n')
		for item in tagCounter.items():
			for i, tree in enumerate(item[1]):
				tree.DisTreeStructure(fOutTrees, 'utf-8')
				if i == 2: break
			
		fOutTrees.write('\n\n\n\n\n\nintersection :\n')
		for item in commons.items():
			for i, tree in enumerate(item[1]):
				tree.DisTreeStructure(fOutTrees, 'utf-8')
				if i == 2: break
			


		fOutTrees.close()
		fOut.close()
		fIn.close()

def usage():
	sys.stderr.write('usage: python CCorpusStater.py  wordTag  inputFile  outputFile\n')
	sys.stderr.write('       or\n')
	sys.stderr.write('       python CCorpusStater.py  nonterminal  inputFile  outputFile\n')


if __name__ == '__main__':

	if len(sys.argv) != 4:
		usage()
		sys.exit(0)

	if sys.argv[1].find('wordTag') != -1:
		CCorpusStater.StatWordInfo(sys.argv[2], sys.argv[3])
	elif sys.argv[1].find('nonterminal') != -1:
		CCorpusStater.StatNonterminals(sys.argv[2], sys.argv[3])
	else:
		usage()

