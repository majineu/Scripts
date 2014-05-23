import sys, os

def ReadStr(line = u''):
	if (len(line) == 0):
		return None

	for ind , ch in enumerate(line):
		if (ch == u' ' or ch == u')'):
			return line[0:ind]

#-----------------------------------------------------------------------------------------------
class CTree(object):
	"""description of class"""
	__slots__ = ('m_isTerminal', 
				 'm_val', 
				 'm_children',
				 'm_parent')

#-----------------------------------------------------------------------------------------------
	def GetChildren(self):
		return self.m_children

#-----------------------------------------------------------------------------------------------
	def RemoveOuterBr(self):
		while self != None and self.m_val == None:
			if self.m_children != None and len(self.m_children) != 0:
				self = self.m_children[0]
			else:
				return None
		return self
		 
#-----------------------------------------------------------------------------------------------
	# input is a unicode string
	@staticmethod
	def BuildTreeHelper(line = ''):
		if (len(line) == 0):
			return None

		(ind, tree, word) = (0, CTree(), '');
		while (ind < len(line)):
			ch = line[ind]
			
			if (ch == ' '):
				ind += 1
				continue

			if (ch == u'('):
				(child, length) = CTree.BuildTreeHelper(line[ind + 1:])
				ind += length + 1
				
				tree.m_isTerminal = False
				child.m_parent = tree
				if (tree.m_children == None):
					tree.m_children = [child]
				else:
					tree.m_children += [child]

				# skip space
				while (ind < len(line)):
					if (line[ind] == ' '):
						ind += 1
						continue
					else:
						break

				continue

			
			if (ch == u')'):
				return (tree, ind + 1)

			# invalid format
			word = ReadStr(line[ind:])
			if (word == None):
				return None

			if (tree.m_val == None):
				tree.m_val = word
				ind += len(word)
			else:
				terminal = CTree(True, word)
				tree.m_children = [terminal]
				tree.m_isTerminal = False
				terminal.m_parent = tree
				return (tree, ind + len(word) + 1)


			ind += 1


#-----------------------------------------------------------------------------------------------
	# input is a unicode string
	@staticmethod
	def ReadingTrees(path =  ''):
		fIn = file(path)
		treeList = []
		sys.stderr.write('Reading trees from %s...' % path)
		for i,line in enumerate(fIn.readlines()):

			tree = CTree.BuildTree(line.strip().decode('utf-8'))
			treeList += [tree]

		sys.stderr.write('Done\n')
		fIn.close()
		return treeList


#-----------------------------------------------------------------------------------------------
	@staticmethod
	def BuildTree(line = ''):  
		line = line.strip()
		if (line[0] == '('):
			return CTree.BuildTreeHelper(line[1:])[0]
		else:
			return None		

#-----------------------------------------------------------------------------------------------
	def __init__(self, isTerminal = None, value = None):
		self.m_isTerminal	= isTerminal
		self.m_val			= value
		self.m_children		= None
		self.m_parent		= None

#-----------------------------------------------------------------------------------------------
	def PrintTree(self, fOut = sys.stderr, English = False):
		
		if (self.m_isTerminal == True):
			if English == True:
				if self.m_parent.m_val.lower().find(u'-lrb-') != -1 :
					fOut.write('-lrb-')
				elif self.m_parent.m_val.lower().find(u'-rrb-') != -1:
					fOut.write('-rrb-')
				else:
					fOut.write((u'%s' %self.m_val).encode('utf-8'))
			else:
				fOut.write((u'%s' %self.m_val).encode('utf-8'))
		else:
			OutStr = u''
			if (self.m_val != None): OutStr = self.m_val
			
			fOut.write((u'(%s '%OutStr).encode('utf-8'))
			for child in self.m_children:
				child.PrintTree(fOut, English)
				
			fOut.write(')')
#-----------------------------------------------------------------------------------------------
	def DisTreeStructure(self, fOut = sys.stderr, outEncoding = 'gbk',  nSpace = 0):
		if (self.m_val == None and nSpace == 0):
			if (self.m_children!= None and len(self.m_children) != 0):
				self.m_children[0].DisTreeStructure(fOut, outEncoding, nSpace)
				return 

		str = u' ' * nSpace
		
		if (self.IsPreterminal() == True):
			fOut.write((str + self.m_val + u' ' + self.m_children[0].m_val).encode(outEncoding) + '\n')
			return
		elif (self.m_val != None):
			fOut.write((str + self.m_val + u'\n').encode(outEncoding))
		

		if (self.m_children != None):
			for child in self.m_children:
				child.DisTreeStructure(fOut, outEncoding,nSpace + 4)

		if (nSpace == 0):
			fOut.write('\n')
		
#-----------------------------------------------------------------------------------------------
	def GetTerminalYield(self):
		terList = []
		self.GetTerminalYieldHelper(terList)
		return terList

#-----------------------------------------------------------------------------------------------
	def GetTerminalYieldHelper(self, terList):
		if (self.m_isTerminal == True):
			terList += [self.m_val]
		else:
			if (self.m_children == None):
				sys.stderr.write('Error: Non-terminal with empty child list\n')
				os.exit(0)
			else:
				for child in self.m_children:
					child.GetTerminalYieldHelper(terList)

#-----------------------------------------------------------------------------------------------
	def GetPreTerminals(self):
		terList = []
		self.GetPreTerminalHelper(terList)
		return terList

#-----------------------------------------------------------------------------------------------
	def GetPreTerminalHelper(self, terList):
		if self.IsPreterminal() == True:
			terList += [self]
		else:
			if self.m_children == None:
				sys.stderr.write('Error: Non-terminal with empty child list\n')
				sys.exit(0)
			else:
				for child in self.m_children:
					child.GetPreTerminalHelper(terList)

#-----------------------------------------------------------------------------------------------
	def IsPreterminal(self):
		return self.m_isTerminal == False and self.m_children != None and len(self.m_children) != 0 and self.m_children[0].m_isTerminal == True

#-----------------------------------------------------------------------------------------------
	def IsNonTerminal(self):
		return self.m_isTerminal == False and self.GetChildNum() != 0 and self.IsPreterminal() == False

#-----------------------------------------------------------------------------------------------
	def IsTerminal(self):
		return self.m_isTerminal 


#-----------------------------------------------------------------------------------------------
	#return terminal node list
	def GetTerminals(self):
		tNodeList = []
		self.GetTerminalsHelper(tNodeList)
		return tNodeList

	def GetTerminalsHelper(self, tNodeList = []):
		if (self.m_isTerminal == True):
			 tNodeList += [self]
		else:
			if (self.m_children == None):
				sys.stderr.write('Error: Non-terminal with empty child list\n')
				os.exit(0)
			else:
				for child in self.m_children:
					child.GetTerminalsHelper(tNodeList)

#-----------------------------------------------------------------------------------------------
	def GetParent(self):
		return self.m_parent

#-----------------------------------------------------------------------------------------------
	def CoverNodeHelper(self, nodeDict = {}):
		if (self in nodeDict):
			del nodeDict[self]

		if (self.m_children != None):
			for child in self.m_children:
				child.CoverNodeHelper(nodeDict)

#-----------------------------------------------------------------------------------------------
	def CoverNodes(self, nodeList = []):
		
		# initialize node list
		nodeDict = {}
		for node in nodeList:
			nodeDict[node] = True

		self.CoverNodeHelper(nodeDict)
		return len(nodeDict) == 0

#-----------------------------------------------------------------------------------------------
	def GetVal (self):
		return self.m_val

#-----------------------------------------------------------------------------------------------
	def CoverChildNodeHelper(self, nodeDict = {}):
		if (self.m_children != None):
			for child in self.m_children:
				if (child in nodeDict):
					delNodeDict[child]
				child.CoverNodeHelper(nodeDict)

#-----------------------------------------------------------------------------------------------
	def CoverChildNodes(self, nodeList = []):
		
		# initialize node list
		nodeDict = {}
		for node in nodeList:
			nodeDict[node] = True

		self.CoverChildNodeHelper(nodeDict)
		return len(nodeDict) == 0
	
#-----------------------------------------------------------------------------------------------
	def GetCommonParent(self, tNodeList = []):
		if (tNodeList == None or len(tNodeList) == 0):
			return None

		if (len(tNodeList) == 1):
			tNodeList[0].m_parent

		(firstNode, tNodeList) = (tNodeList[0], tNodeList[1:])
		
		while (firstNode != None):
			if (firstNode.CoverChildNodes(tNodeList) == True):
				return firstNode
			else:
				firstNode = firstNode.m_parent
		
		return None		

#-----------------------------------------------------------------------------------------------
	def SelfDelete(self):
		root = self
		while (root.m_parent != None):
			root = root.m_parent

		if (self.SelfDeleteHelper() == False):
			return None
		else:
			return root
#-----------------------------------------------------------------------------------------------
	def SelfDeleteHelper(self):
		parent = self.m_parent
		# check if parent is root
		if (parent == None):
			self = None
			return False

		# otherwise, parent should never be None
		# and remove the child node from childlist
		for i,child in enumerate(parent.m_children):
			if (child == self):
				del parent.m_children[i]
				break

		# check if parent has no child left
		if (len(parent.m_children) == 0):
			parent.m_children = None
			return parent.SelfDeleteHelper()
		
		return True

#-----------------------------------------------------------------------------------------------
	def IsEmptyTree(self):
		return self.m_val == None and self.m_children == None and self.m_parent == None


#-----------------------------------------------------------------------------------------------
	def SetVal(self, val = ''):
		self.m_val = val

#-----------------------------------------------------------------------------------------------
	def Copy_InsertNewTerminalToTree(self):
		preTerminal = self.m_parent
		nonTerminal = preTerminal.m_parent

		childIndex = 0
		for i, child in enumerate(nonTerminal.m_children):
			if (child == preTerminal):
				childIndex = i
				break
		
		# copy preterminal and insert to nonTerminal's child list
		newPreTerminal = CTree(False, preTerminal.m_val)
		newPreTerminal.m_parent = nonTerminal
		nonTerminal.m_children.insert(childIndex + 1, newPreTerminal)
		
		# copy terminal and set it as the new pre-terminal's child
		newTerminal = CTree(True, self.m_val)
		newTerminal.m_parent = newPreTerminal
		newPreTerminal.m_children = [newTerminal]

		return newTerminal

#-----------------------------------------------------------------------------------------------
	def GetPreOrderTreeList(self):
		nodeList = []
		self.GetPreOrderTreeListHelper(nodeList)
		return nodeList

#-----------------------------------------------------------------------------------------------
	def GetPreOrderTreeListHelper(self, nodeList = []):
		if (self.m_val != None):
			nodeList += [self]

		if (self.m_children != None):
			for child in self.m_children:
				child.GetPreOrderTreeListHelper(nodeList)

#-----------------------------------------------------------------------------------------------
	# removing self-loop unary rules
	def RemoveSelfLoops(self):
		if self.IsPreterminal() or self.IsTerminal():
			return

		if self.m_children == None or len(self.m_children) == 0:
			return

		head = ''
		if self.m_val != None: head = self.m_val.split(u'_')[0]
		
		while len(self.m_children) == 1 and self.m_children[0].m_val.split(u'_')[0] == head:
			# set new children
			self.m_children[0].m_parent = None
			self.m_children				= self.m_children[0].m_children
				
			# set new parent
			for child in self.m_children:
				child.m_parent = self

		# recursive call
		for child in self.m_children:
			child.RemoveSelfLoops()

#-----------------------------------------------------------------------------------------------
	# removing self-loop unary rules
	def ContainSelfLoops(self):
		if self.IsPreterminal() or self.IsTerminal():
			return False

		if self.m_children == None or len(self.m_children) == 0:
			return False

		head = ''
		if self.m_val != None: head = self.m_val.split(u'_')[0]
		
		if len(self.m_children) == 1 and self.m_children[0].m_val.split(u'_')[0] == head:
			return True

		# recursive call
		containFlag = False
		for child in self.m_children:
			containFlag = containFlag or child.ContainSelfLoops()
		return containFlag

#-----------------------------------------------------------------------------------------------
	def GetNodeAtDepth(self, depth = 0):
		nodeList = []
		self.GetNodeAtDepthHelper(depth, nodeList)
		return nodeList

#-----------------------------------------------------------------------------------------------
	def GetNodeAtDepthHelper(self,  depth, nodeList = [], currentDep = 0):
		if depth < currentDep:
			return

		elif depth == currentDep:
			nodeList += [self]
			
		elif self.m_isTerminal == False:
			for child in self.m_children:
				child.GetNodeAtDepthHelper(depth, nodeList, currentDep + 1)

#-----------------------------------------------------------------------------------------------
	def GetChildren(self, index):
		if self.m_children == None or len(self.m_children) <= index:
			return None
		return self.m_children[index]

#-----------------------------------------------------------------------------------------------
	def GetTagWordList(self):
		preTerminals = self.GetPreTerminals()
		wordTagList = [(node.GetChildren(0).GetVal(), node.GetVal()) for node in preTerminals]
		return wordTagList


#-----------------------------------------------------------------------------------------------
	def GetChildNum(self):
		if self.m_children == None or len(self.m_children) == 0:
			return 0
		return len(self.m_children)

#-----------------------------------------------------------------------------------------------
	def GetSpans(self):
		spanList = []
		self.GetSpansHelper(spanList)
		return spanList

#-----------------------------------------------------------------------------------------------
	def GetSpansHelper(self, spanList = [], begIndex = 0):
		if self.IsPreterminal() == True or self.IsTerminal() == True:
			return

		if self.m_val == None:
			if self.GetChildNum() != 0:
				self.m_children[0].GetSpansHelper(spanList) 
		
		index = begIndex
		if self.GetChildNum() != 0:
			for child in self.m_children:
				child.GetSpansHelper(spanList,  index)
				index += len(child.GetTerminals())
			spanList += [(self,  begIndex,  index)]



