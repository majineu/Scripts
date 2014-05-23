from TreeClass import *

class CPattern:

	@staticmethod
	def ReadPattern(patternPath):

		f = file(patternPath)
		keyWordList = []
		for line in f:
			words = re.split('\s+',  line.strip().decode('utf-8'))
			if (len(words) < 2):
				keyWordList += [u'']
			else:
				keyWordList += [words[1]]

		print keyWordList
		pattern = CPattern(keyWordList[0], keyWordList[1], keyWordList[2], keyWordList[3], keyWordList[4], keyWordList[5], keyWordList[6])
		sys.stderr.write(str(pattern).decode('utf-8').encode('gbk')+ '\n')
		return pattern


	def __init__(self, wHead = u'', tHead = u'', wChild = u'', tChild = u'',  wGrandChild= u'', tGrandChild= u'', dir = u''):
		self.wHead	= wHead
		self.tHead	= tHead
		self.wChild = wChild
		self.tChild = tChild
		self.tGrandChild = tGrandChild
		self.wGrandChild = wGrandChild
		self.dir	= dir

	
	def __str__(self):
		resStr = u''
		if (self.wHead != u''):
			resStr = u'wH_' + self.wHead

		if (self.tHead != u''):
			resStr += u'_tH_' + self.tHead

		resStr += u'___'
		if (self.wChild != u''):
			resStr += u'_wC_' + self.wChild

		if (self.tChild != u''):
			resStr += u'_tC_' + self.tChild

		if self.tGrandChild != u'':
			resStr += u'_tG_' + self.tGrandChild
			
		if self.wGrandChild != u'':
			resStr += u'_wG_' + self.wGrandChild
			
			
		resStr += u'_dir_' + self.dir
		return resStr.encode('utf-8')



def GetPatternFromTree(tree, pattern = CPattern(), resTreeList = []):
	wHead, tHead = tree.GetWord(), tree.GetTag()

	for dir in [u'l', u'r']:
		children = []

		if (dir == u'l'):
			children = tree.GetLeftChildren()
		else:
			children = tree.GetRightChildren()

		if (pattern.dir == u'l' and dir != u'l'):
			continue

		if (pattern.dir == u'r' and dir != u'r'):
			continue

		# recursive call: collect pattern from child trees
		for child in children:
			GetPatternFromTree(child, pattern , resTreeList)


		for child in children:
			wChild = child.GetWord()
			tChild = child.GetTag()
			
			if (pattern.wHead != u'' and pattern.wHead != wHead):
				continue
			
#			if (pattern.tHead != u'' and pattern.tHead != tHead):
			if (pattern.tHead != u'' and tHead.find(pattern.tHead) != 0):
				continue
		
			if (pattern.wChild != u'' and pattern.wChild != wChild):
				continue

#			if (pattern.tChild != u'' and pattern.tChild != tChild):
			if (pattern.tChild != u'' and tChild.find(pattern.tChild) != 0):
				continue
			
			match = True
			if pattern.tGrandChild != u'' or pattern.wGrandChild != u'':
				match = False
				
				# process left grand children
				grands = child.GetLeftChildren()
				for gChild in grands:
					if gChild.GetTag().find(pattern.tGrandChild) == 0 and gChild.GetWord().find(pattern.wGrandChild) == 0:
						match = True
						break
				
				# process right grand children
				if match == True:
					resTreeList += [tree]
				else:
					grands = child.GetRightChildren()
					for gChild in grands:
						if gChild.GetTag().find(pattern.tGrandChild) == 0 and gChild.GetWord().find(pattern.wGrandChild) == 0:
							match = True
							break
				
			if match == True:
				resTreeList += [tree]
				break
			
		
def GetPattern(treePath, pattern = CPattern()):
	
	TreeList = Tree.ReadTreesFromFile(treePath)
	treesHit = []
	
	for i, tree in enumerate(TreeList):
		if (i != 0 and i % 2000 == 0):
			sys.stderr.write(str(i) + '\r')

		GetPatternFromTree(tree, pattern, treesHit)

	return treesHit


if (__name__ == '__main__'):
	
	if (len(sys.argv) != 4):
		sys.stderr.write('usage: python  PatternCollector.py  treePath   patternPath  resDir')
		sys.exit(0)

	pattern = CPattern.ReadPattern(sys.argv[2])
	treesHit = GetPattern(sys.argv[1],  pattern)
	fOut = file(sys.argv[3] + '\\' + str(pattern).decode('utf-8').encode('gbk').strip(), 'w')

	fOut.write('total ' + str(len(treesHit)) + ' cases\n')
	sys.stderr.write('total ' + str(len(treesHit)) + ' cases\n')
	for tree in treesHit:
		tree.PrintTree(0,0, fOut)
		fOut.write('\n\n')

	fOut.close()




