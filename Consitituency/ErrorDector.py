from Tree import *
from CSigHanTrans import *
from CCorpusStater import *

class CErrorDector(object):
	"""description of class"""

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def ComparePOS(pathGold, pathGuess, resPath):
		fGold	= file(pathGold)
		fGuess	= file(pathGuess)
		fRes	= file(resPath, 'w')
		confuse = {}
		for i, linePair in enumerate(zip(fGold, fGuess)):
			if i != 0 and i % 1000 == 0:
				sys.stderr.write('processing line %d ...\r' %i)

			treeGold	= CTree.BuildTree(linePair[0].strip().decode('utf-8'))
			treeGold	= treeGold.RemoveOuterBr()
			treeGuess	= CTree.BuildTree(linePair[1].strip().decode('utf-8'))
			treeGuess	= treeGuess.RemoveOuterBr()

			if treeGold == None or treeGuess == None:
				sys.stderr.write('line %d contains empty tree\n' %i)
				continue

			flags = CErrorDector.ComparePOSPerTree(treeGold, treeGuess)
			
			if False in flags:
				fRes.write('\n sentence %d\n' %i)
				for i, nodePair in enumerate(zip(treeGold.GetTagWordList(), treeGuess.GetTagWordList())):
					outStr = nodePair[0][0] + u'_' + nodePair[0][1] + u'\t\t' + nodePair[1][0] + u'_' + nodePair[1][1]

					if flags[i] == False:
						outStr += u'\t####################################'

						tagPair = nodePair[0][1] + u'  ' + nodePair[1][1]
						if tagPair in confuse:
							confuse[tagPair] += 1
						else:
							confuse[tagPair] = 1 

					fRes.write(outStr.encode('utf-8') + '\n')

				fRes.write('\n')
		sortConfuse = sorted(confuse.items(), key = lambda x:x[1], reverse = True)
		for item in sortConfuse:
			fRes.write((u'%s\t\t:\t%d' %(item[0], item[1])).encode('utf-8') + '\n')

		fGold.close()
		fGuess.close()
		fRes.close()

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def ComparePOSPerTree(treeGold = CTree(), treeGuess = CTree()):
		preTerminalsGold	= treeGold.GetPreTerminals()
		preTerminalsGuess	= treeGuess.GetPreTerminals()
		flags = [nodePair[0].GetVal() == nodePair[1].GetVal() for nodePair in zip(preTerminalsGold, preTerminalsGuess)]
		return flags

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def eqSpan(sp1 = (CTree(), 0, 0), sp2 = (CTree(), 0, 0)):
		return sp1[0].GetVal() == sp2[0].GetVal() and sp1[1] == sp2[1] and sp1[2] == sp2[2]

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def SpanErrors(treeGold = CTree(), treeGuess = CTree()):
		goldSpans = treeGold.GetSpans()
		testSpans = treeGuess.GetSpans()

		extraSpans	= []
		lostSpans	= []
		commons		= []

		for goldSpan in goldSpans:
			flag = False
			for testSpan in testSpans:
				if CErrorDector.eqSpan(goldSpan, testSpan) == True:
					flag = True
					break
			
			if flag == False:
				lostSpans += [goldSpan]
			else:
				commons += [goldSpan]
		
		for testSpan in testSpans:
			flag = False
			for goldSpan in goldSpans:
				if CErrorDector.eqSpan(goldSpan, testSpan) == True:
					flag = True
					break

			if flag == False:
				extraSpans += [testSpan]

		return (extraSpans, lostSpans, commons)

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def LowestSpans(spans = []):
		
		lowest = []
		for span1 in spans:
			containChildSpan = False
			for span2 in spans:
				if span2[0].GetParent() == span1[0]:
					containChildSpan = True
					break

			if containChildSpan == False:
				lowest += [span1]
		return lowest

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def DetectSpanErrors(pathGold, pathGuess, resPath):
		fGold	= file(pathGold)
		fGuess	= file(pathGuess)
		fRes	= file(resPath, 'w')
		confuse = {}

		(totalCorr, totalGuess, totalGold) = (0,0,0)
		for i, linePair in enumerate(zip(fGold, fGuess)):
			if i != 0 and i % 1000 == 0:
				sys.stderr.write('processing line %d ...\r' %i)

			treeGold	= CTree.BuildTree(linePair[0].strip().decode('utf-8'))
			treeGold	= treeGold.RemoveOuterBr()
			treeGuess	= CTree.BuildTree(linePair[1].strip().decode('utf-8'))
			treeGuess	= treeGuess.RemoveOuterBr()

			if treeGold == None or treeGuess == None:
				sys.stderr.write('line %d contains empty tree\n' %i)
				continue
			
			(extraSpans, lostSpans, commons) = CErrorDector.SpanErrors(treeGold, treeGuess)



			if len(extraSpans) != 0 or len(lostSpans) != 0:
				fRes.write('sentence----------------------------------------------------- %d\nGold:::::::::::::::\n' %i)
				treeGold.DisTreeStructure(fRes, 'utf-8')
				fRes.write('Guess::::::::::::::\n')
				treeGuess.DisTreeStructure(fRes, 'utf-8')
				
				if len(extraSpans) != 0:
					fRes.write('extras::::::::::::::\n')
					for span in extraSpans:
						span[0].DisTreeStructure(fRes, 'utf-8')
						
				if len(lostSpans) != 0:
					fRes.write('losts::::::::::::::\n')
					for span in lostSpans:
						span[0].DisTreeStructure(fRes, 'utf-8')
						
		fRes.close()
		fGold.close()
		fGuess.close()

#-----------------------------------------------------------------------------------------------
	@staticmethod
	def ContainTagingError(spans = [], tagDict = {}, tagPairs = []):
		for span in spans:
			for i in range(span[1], span[2], 1):
				if tagPairs[i][0] != tagPairs[i][1]:
					if tagPairs[i][0] + '_'+ tagPairs[i][1] in tagDict:
						tagDict [tagPairs[i][0] + '_'+ tagPairs[i][1]] += 1
					else:
						tagDict [tagPairs[i][0] + '_'+ tagPairs[i][1]] = 1


	@staticmethod
	def Scoring(trainingPath, pathGold, pathGuess, resPath, toCourseType = False):
		fGold	= file(pathGold)
		fGuess	= file(pathGuess)
		fRes	= file(resPath, 'w')

		trainingTrees = CTree.ReadingTrees(trainingPath)
		wCounter = {}
		for tree in trainingTrees:
			CCorpusStater.StatWordPerTree(tree, wCounter)


		confuse = {}
		print 'Scoring....'

		(totalCorr, totalGuess, totalGold) = (0,0,0)
		tagInErrorSpanList = {}

		for i, linePair in enumerate(zip(fGold, fGuess)):
			if i != 0 and i % 1000 == 0:
				sys.stderr.write('processing line %d ...\r' %i)

			treeGold	= CTree.BuildTree(linePair[0].strip().decode('utf-8'))
			treeGold	= treeGold.RemoveOuterBr()
			treeGuess	= CTree.BuildTree(linePair[1].strip().decode('utf-8'))
			treeGuess	= treeGuess.RemoveOuterBr()

			if treeGold == None or treeGuess == None:
				sys.stderr.write('line %d contains empty tree\n' %i)
				continue
				
			if (toCourseType):
				CSigHanTrans.Transformat(treeGold)
				CSigHanTrans.Transformat(treeGuess)

			# find POS tag errors
			goldTags	= [elem[1] for elem in treeGold.GetTagWordList()]
			guessTags	= [elem[1] for elem in treeGuess.GetTagWordList()]

			

			# find span errors
			(extraSpans, lostSpans, commons) = CErrorDector.SpanErrors(treeGold, treeGuess)

			goldPreterminals = treeGold.GetPreTerminals()
			guessPreterminals = treeGuess.GetPreTerminals()
			for nodes in zip(goldPreterminals, guessPreterminals):
				if nodes[0].GetVal() != nodes[1].GetVal():
					if nodes[1].GetChildren(0).GetVal() not in wCounter:
						nodes[1].SetVal(nodes[1].GetVal() + u'^^^^'+nodes[0].GetVal() + u'  OOV ||||  ')
					else:
						nodes[1].SetVal(nodes[1].GetVal() + u'^^^^'+nodes[0].GetVal())
						
						


			# compute scores
			totalCorr += len(commons)
			totalGold += len(commons) + len(lostSpans)
			totalGuess+= len(commons) + len(extraSpans)

			if len(extraSpans) != 0 or len(lostSpans) != 0:
				fRes.write('sentence----------------------------------------------------- %d\nGold:::::::::::::::\n' %i)
				treeGold.DisTreeStructure(fRes, 'utf-8')
				fRes.write('Guess::::::::::::::\n')
				treeGuess.DisTreeStructure(fRes, 'utf-8')
				
				if len(extraSpans) != 0:
					fRes.write('extras::::::::::::::\n')
					for span in extraSpans:
						span[0].DisTreeStructure(fRes, 'utf-8')
						
				if len(lostSpans) != 0:
					fRes.write('losts::::::::::::::\n')
					for span in lostSpans:
						span[0].DisTreeStructure(fRes, 'utf-8')

			lowestLost	= CErrorDector.LowestSpans(lostSpans)
			lowestExtra = CErrorDector.LowestSpans(extraSpans)
			
			CErrorDector.ContainTagingError(lowestLost, tagInErrorSpanList, zip(goldTags, guessTags))
		
		fRes.write('corr %d, gold %d, totalGuess %d,  recall %.2f%%,  prec %.2f%%,  f1 %.2f%%\n'
					%(totalCorr, totalGold, totalGuess, 100.0 * totalCorr/totalGold, 100.0 * totalCorr/totalGuess, 
						100.0 * 2 * totalCorr/(totalGold + totalGuess)))
		sortedTagErrors = sorted(tagInErrorSpanList.items(), key = lambda x: x[1], reverse = True)

		for item in sortedTagErrors:
			fRes.write((u'%s %d\n' %(item[0], item[1])).encode('utf-8'))

		fRes.close()
		fGold.close()
		fGuess.close()






