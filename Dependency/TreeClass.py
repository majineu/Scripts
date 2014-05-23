import sys, re, os

class Tree:
	"""a simple dependency tree class for common use"""

	@staticmethod
	def ReadTreesFromFile(filePath, conllFormat = False):
		
		sys.stderr.write('Reading dependency trees from ' + filePath + '\n')
		fIn = file(filePath)
		tupleList	= []
		treeList	= []
		treeNum		= 0
		for i, line in enumerate (fIn):
			items = filter(lambda x: len(x) != 0, re.split('\s+', line.decode('utf-8')))
			if (len(items) == 0):
				if (len(tupleList) != 0):
					tree = Tree.BuildTree(tupleList)
			
					if (tree != None):
						treeList += [tree]
						treeNum += 1
						if (treeNum % 1000 == 0):
							sys.stderr.write (str(treeNum) + '\r')

					tupleList = []
				continue


			if (conllFormat == False):
				tupleList += [(items[0], items[1], items[2], items[3])]
			else:
				tupleList += [(items[1], items[3], items[6], items[7])]


		# process the last one
		if (len(tupleList) > 0):
			tree = Tree.BuildTree(tupleList)
			if (tree != None):
				treeList += [tree]

		return treeList


	# each tuple is (word, tag, headindex deplabel)
	@staticmethod
	def BuildTree(tupleList):
		treeList = []
		for index, tuple in enumerate(tupleList):
			treeList += [Tree(index, tuple[0], tuple[1], int(tuple[2]), tuple[3])]

		head = None
		for index, tree in enumerate(treeList):
			if (tree.headIndex != 0):
				tree.headIndex -= 1

				if (tree.headIndex > index):
					treeList[tree.headIndex].PushBackLeftChild(tree)
				else:
					treeList[tree.headIndex].PushBackRightChild(tree)
			else:
				head = tree

		return head

	


	def __init__(self, wordIndex, word, tag, headIndex, depLabel):
		self.word		= word
		self.tag		= tag
		self.headIndex	= headIndex
		self.depLabel	= depLabel
		self.wordIndex  = wordIndex
		self.parent		= None
		self.left_children   = []
		self.right_children  = []

	

	def PushBackLeftChild(self, tree):
		self.left_children += [tree]
		tree.parent = self


	def PushBackRightChild(self, tree):
		self.right_children += [tree]
		tree.parent = self


	def PushFrontLeftChild(self, tree):
		self.left_children = [tree] + self.left_children
		tree.parent = self


	def IsLeaf(self):
		return len(self.left_children) == 0 and len(self.right_children) == 0


	def GetChildNum(self):
		return len(self.left_children) + len(self.right_children)


	def GetLeftChildNum(self):
		return len(self.left_children)


	def GetRightChildNum(self):
		return len(self.right_children)


	def GetLeftChildren(self):
		return self.left_children


	def GetRightChildren(self):
		return self.right_children


	def GetParent(self):
		return self.parent

	
	def GetWord(self):
		return self.word


	def GetTag(self):
		return self.tag


	def PrintTree(self, depth = 0, direction = 0, f = sys.stderr):
		for tree in self.left_children:
			tree.PrintTree(depth + 1, 1, f)

		if (depth > 0):
			if (direction == 1):
				f.write( ' ' * 4 * depth + '/---')
			elif (direction == 2):
				f.write( ' ' * 4 * depth + '\\---')

		f.write("[%s   %s   %s   %d]\n" %(self.word.encode('utf-8'), self.tag.encode('utf-8'), self.depLabel.encode('utf-8'), self.headIndex) )

		for tree in self.right_children:
			tree.PrintTree(depth + 1, 2, f)


	def GetNodes(self, nodeList):
		for tree in self.left_children:
			tree.GetNodes(nodeList)

		nodeList += [[self.word, self.tag, self.headIndex, self.depLabel]]

		for tree in self.right_children:
			tree.GetNodes(nodeList)

			 




