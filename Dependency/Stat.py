from TreeClass import *

def StatBiLex_BiPosFromTree(tree, biLexDict, biPOSDict, biLexPOSDict):
	
	headWord, headTag = tree.GetWord(), tree.GetTag()
	for child in tree.GetLeftChildren():
		if (child.GetTag() == 'PU'):
			continue

		biPOS		= headTag  + u'---' + u'L_' + child.GetTag()
		biLex		= headWord + u'---' + u'L_' + child.GetWord()
		biLexPOS	= headWord + u'_' + headTag + u'---' + u'L_' + child.GetWord() + u'_' + child.GetTag()

		if (biPOS in biPOSDict):
			biPOSDict[biPOS] += 1.0
		else:
			biPOSDict[biPOS] = 1.0

		if (biLex in biLexDict):
			biLexDict[biLex] += 1.0
		else:
			biLexDict[biLex] = 1.0


		if (biLexPOS in biLexPOSDict):
			biLexPOSDict[biLexPOS] += 1.0
		else:
			biLexPOSDict[biLexPOS] = 1.0


	for child in tree.GetRightChildren():
		if (child.GetTag() == 'PU'):
			continue

		biPOS = headTag  + u'---' + u'R_' + child.GetTag()
		biLex = headWord + u'---' + u'R_' + child.GetWord()
		biLexPOS	= headWord + u'_' + headTag + u'---' + u'R_' + child.GetWord() + u'_' + child.GetTag()

		if (biPOS in biPOSDict):
			biPOSDict[biPOS] += 1.0
		else:
			biPOSDict[biPOS] = 1.0

		if (biLex in biLexDict):
			biLexDict[biLex] += 1.0
		else:
			biLexDict[biLex] = 1.0

		if (biLexPOS in biLexPOSDict):
			biLexPOSDict[biLexPOS] += 1.0
		else:
			biLexPOSDict[biLexPOS] = 1.0




def OutputDict(dict, outPath):
	fOut = file(outPath, 'w')

	sortedList = sorted(dict.items(), key = lambda x:x[1], reverse = True) # by value, descending order 
	for item in sortedList:
		fOut.write((item[0] + u'\t\t\t' + unicode(item[1])).encode('utf-8') + '\n')
	
	fOut.close()



def StatBiLex_POS(treePath, bi_LexPath, bi_POSPath, bi_LexPOSPath = ''):
	
	TreeList = Tree.ReadTreesFromFile(treePath)
	
	biLexDict		= {}
	biPOSDict		= {}
	biLexPOSDict	= {}

	for i, tree in enumerate(TreeList):
		if (i != 0 and i % 10000 == 0):
			sys.stderr.write(str(i) + '\r')

		StatBiLex_BiPosFromTree(tree, biLexDict, biPOSDict, biLexPOSDict)

	OutputDict(biLexDict, bi_LexPath)
	OutputDict(biPOSDict, bi_POSPath)

	if (bi_LexPOSPath != ''):
		OutputDict(biLexPOSDict, bi_LexPOSPath)





if (__name__ == '__main__'):
	
	if (len(sys.argv) not in [4, 5]):
		sys.stderr.write('usage: python Stat.py  treePath  bi-lexPath  bi-POSPath (bi-LexPOS)\n')
		sys.stderr.write(' note: all files are in utf-8 format\n')
		sys.exit(0)

	if (len(sys.argv) == 4):
		StatBiLex_POS(sys.argv[1], sys.argv[2], sys.argv[3])
	elif (len(sys.argv) == 5):
		StatBiLex_POS(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])







