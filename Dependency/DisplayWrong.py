from TreeClass import *


def ReadSentenceList(path,  senList = [],  flagConll = False):
	fin	= file(path)
	sentence = []
	print 'reading from %s...' %path
	for i, line in enumerate(fin):
		if (i != 0 and i % 10000 == 0):
			sys.stderr.write('%d\r' %i)
			#break

		items = filter(lambda x: x != '',  re.split('\s+', line.decode('utf-8')));
	
		#if (i > 10000):
		#	sys.stderr.write('\nGot here\n')
				
		if (len(items) == 0):
			if(len(sentence) != 0):
				senList += [sentence]
				sentence = []
		else:

			if (flagConll == True):
				node = [items[1], items[3], items[6], items[7]]
			else:
				node = [items[0], items[1], items[2], items[3]]
			
			sentence += [node]	

	sys.stderr.write('\ndone\n')
	fin.close()




def CompareWithGold(goldSen, guessSen, resList = []):
	puncs = [",", ".", ":", "``", "''", "-LRB-", "-RRB-", "PU"]

	for nodePair in zip(goldSen, guessSen):
		#	nodePair[0] gold node  (word, tag, dep, depLabel)
		#	nodePair[1] guess node (word, tag, dep, depLabel)
		#	print len(nodePair[0])
		if (nodePair[0][1] not in puncs):
			#	if tag wrong, if headIndex wrong
			resList += [(nodePair[0][1] == nodePair[1][1], nodePair[0][2] == nodePair[1][2])]
		else:
			resList += [(nodePair[0][1] == nodePair[1][1], None)]


def CompareTwoRes(goldPath, guessPath1, guessPath2, difGoldPath, difWrongPath1, difWrongPath2):
	puncs = [",", ".", ":", "``", "''", "-LRB-", "-RRB-", "PU"]

	goldSenList		= []
	guessSenList1	= []
	guessSenList2	= []
	
	ReadSentenceList(goldPath, goldSenList)
	ReadSentenceList(guessPath1, guessSenList1)
	ReadSentenceList(guessPath2, guessSenList2)

	fDifGold	= file(difGoldPath,  'w')
	fWrong1		= file(difWrongPath1, 'w')
	fWrong2		= file(difWrongPath2, 'w')

	cmpCounter = [0,     0,   0,   0]
	cmpString = ['--','-+','+-','++']

	cmpPOSCounter = [0,     0,   0,   0]
	cmpPOSString =  ['--','-+','+-','++']


	for i in range(0, len(goldSenList), 1):
		cmpList1, cmpList2 = [], []
		
		CompareWithGold(goldSenList[i], guessSenList1[i], cmpList1)
		CompareWithGold(goldSenList[i], guessSenList2[i], cmpList2)

		score1 = len(filter(lambda x: x[1] == True, cmpList1))
		score2 = len(filter(lambda x: x[1] == True, cmpList2))

		for resPair in zip(cmpList1, cmpList2):
			if (resPair[0][1]  != None):
				# the two indexes is 
				# resPair[0][1]: the first dependency is correct
				# resPair[0][1]: the second dependency is correct
				cmpCounter[resPair[0][1] * 2 + resPair[1][1]] += 1.0

			# resPair[0][0]: the first dependency is correct
			# resPair[0][0]: the second dependency is correct
			cmpPOSCounter[resPair[0][0] * 2 + resPair[1][0]] += 1.0
		
		
		if cmpList1 != cmpList2:

			for k, nodeResPair in enumerate(zip(guessSenList1[i], cmpList1)):
			
				# nodeResPair[1][0] : Dependency correct flag 
				# nodeResPair[1][1] : POS tag correct flag
				if (nodeResPair[1][0] == False or nodeResPair[1][1] == False):
				
					if (nodeResPair[1][0] == False):
						completeMatch = False
						guessSenList1[i][k][3] += '       pppppppppppppppppppp   '

					if (nodeResPair[1][1] == False):
						guessSenList1[i][k][3] += '       --------------------   '


			for k, nodeResPair in enumerate(zip(guessSenList2[i], cmpList2)):
			
				# nodeResPair[1][0] : Dependency correct flag 
				# nodeResPair[1][1] : POS tag correct flag
				if (nodeResPair[1][0] == False or nodeResPair[1][1] == False):
				
					if (nodeResPair[1][0] == False):
						completeMatch = False
						guessSenList2[i][k][3] += '       pppppppppppppppppppp   '

					if (nodeResPair[1][1] == False):
						guessSenList2[i][k][3] += '       --------------------   '


			fDifGold.write('\n\n\nsentence %d--------------------\n' %i)
			fWrong1.write('\n\n\nsentence %d-------------------- score %d' %(i,score1))
			fWrong2.write('\n\n\nsentence %d-------------------- score %d' %(i,score2))


			if (score1 > score2):
				fWrong1.write('  better \n' )
				fWrong2.write('\n')
			else:
				fWrong2.write('  better\n')
				fWrong1.write('\n')


			goldTree	= Tree.BuildTree(goldSenList[i])
			guessTree1	= Tree.BuildTree(guessSenList1[i])
			guessTree2	= Tree.BuildTree(guessSenList2[i])
			
			goldTree.PrintTree(0,0, fDifGold)
			guessTree1.PrintTree(0,0, fWrong1)
			guessTree2.PrintTree(0,0, fWrong2)

	print 'Menemar test for dependency:'
	for matchString_countPair in zip(cmpString, cmpCounter):
		sys.stderr.write('%s:%d  \n' %(matchString_countPair[0], matchString_countPair[1]))

	print '\nMenemar test for tagging:'
	for matchString_countPair in zip(cmpPOSString, cmpPOSCounter):
		sys.stderr.write('%s:%d  \n' %(matchString_countPair[0], matchString_countPair[1]))
	sys.stderr.write('\n')

	fDifGold.close()
	fWrong1.close()
	fWrong2.close()



	
def GetWrong(goldPath, guessPath, difGoldPath, difWrongPath):

	goldSenList		= []
	guessSenList	= []
	ReadSentenceList(goldPath, goldSenList)
	ReadSentenceList(guessPath, guessSenList)

	fDifGold	= file(difGoldPath,  'w')
	fWrong		= file(difWrongPath, 'w')

	for i, senPair in enumerate(zip(goldSenList, guessSenList)):
		cmpList = []
		CompareWithGold(senPair[0], senPair[1], cmpList)

		completeMatch = True
		# locate attached word
		for k, nodeResPair in enumerate(zip(senPair[1], cmpList)):
			
			# nodeResPair[1][0] : Dependency correct flag 
			# nodeResPair[1][1] : POS tag correct flag
			if (nodeResPair[1][0] == False or nodeResPair[1][1] == False):
				completeMatch = False
				if (nodeResPair[1][0] == False):
					senPair[1][k][3] += '       pppppppppppppppppppp   '
					13
				if (nodeResPair[1][1] == False):
					senPair[1][k][3] += '       --------------------   '

		
		if (completeMatch == False):
			fWrong.write('sentence %d--------------------\n' %i)
			fDifGold.write('sentence %d--------------------\n' %i)
			
			goldTree	= Tree.BuildTree(senPair[0])
			guessTree	= Tree.BuildTree(senPair[1])
			
			goldTree.PrintTree(0,0, fDifGold)
			guessTree.PrintTree(0,0, fWrong)

			fDifGold.write('\n\n\n')
			fWrong.write('\n\n\n')
			

	fDifGold.close()
	fWrong.close()



if (__name__ == '__main__'):
	if (len(sys.argv) not in [6, 8]):
		sys.stderr.write ('usage:\npython  DisplayWrong.py  disWrong goldFile  testFile  difGoldFile  difWrongFile\n')
		sys.stderr.write ('or\npython  DisplayWrong.py  cmpTwoResults goldFile  test1  test2  difGold  difTest1 difTest2\n')
		sys.exit(1)

	if (sys.argv[1] == 'disWrong'):
		# arguments: goldPath,  guessPath,  difGoldPath,  difWrongPath
		GetWrong(sys.argv[2],  sys.argv[3],  sys.argv[4],  sys.argv[5])
	elif (sys.argv[1] == 'cmpTwoResults'):
		# arguments:  goldPath, guessPath1, guessPath2, difGoldPath, difWrongPath1, difWrongPath2
		CompareTwoRes(sys.argv[2],  sys.argv[3],  sys.argv[4],  sys.argv[5], sys.argv[6],  sys.argv[7]) 
				











	