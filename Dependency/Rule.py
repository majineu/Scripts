from Tree import *


class CRule(object):
	"""description of class"""
	__slots__ = ('m_nChild',		# how many right nonterminals
				 'm_head',			# left nonterminal
				 'm_childList')		# 

#--------------------------------------------------------------------------------------------------
	def __init__(self, head = u'', childList = None):
		self.m_head		 = head
		self.m_childList = childList
		if self.m_childList == None:
			self.m_nChild = 0
		else:
			self.m_nChild = len(self.m_childList)
#--------------------------------------------------------------------------------------------------
	def IsUnary(self):
		return self.m_nChild == 1

	def __eq__(self, other):
		#print 'called'
		return self.m_nChild == other.m_nChild and self.m_head == other.m_head and cmp(self.m_childList, other.m_childList) == 0

#--------------------------------------------------------------------------------------------------
	def __cmp__(self, r):
		if (cmp(self.m_nChild, r.m_nChild) == 0):
			if (cmp(self.m_childList, r.m_childList) == 0):
				return cmp(self.m_head, r.m_head)
			else:
				return cmp(self.m_childList, r.m_childList)
		else:
			return cmp(self.m_nChild, r.m_nChild)

	def __hash__(self):
		return self.toString().__hash__()


#--------------------------------------------------------------------------------------------------
	def __str__(self):
		string = u''
		if (self.m_head != None):
			string += self.m_head
		if (self.m_childList != None):
			string += u'->' + u'_'.join(self.m_childList)
		return string

	def toString(self):
		string = u''
		if (self.m_head != None):
			string += self.m_head
		if (self.m_childList != None):
			string += u'->' + u'_'.join(self.m_childList)
		return string

#--------------------------------------------------------------------------------------------------
	def GetHead(self):
		return self.m_head

#--------------------------------------------------------------------------------------------------
	def SetHead(self, head = u''):
		self.m_head = head

#--------------------------------------------------------------------------------------------------
def CollectRule(tree = CTree()):
	if (tree.IsTerminal() == True):
		return None

	ruleList = []
	CollectRuleHelper(tree, ruleList)
	return ruleList
	
#--------------------------------------------------------------------------------------------------
def CollectRuleHelper(tree = CTree(), ruleList = []):
	if (tree.IsPreterminal() == True or tree.IsTerminal() == True):
		return None

	if (tree.GetVal() == None):
		if (tree.GetChildren() == None or len(tree.GetChildren()) == 0):
			return 
		else:
			tree = tree.GetChildren()[0]

	children = tree.GetChildren()
	(head ,right) = (tree.GetVal().split('_')[0], [])
	for child in children:
		CollectRuleHelper(child, ruleList)
		right += [child.GetVal().split('_')[0]]

	ruleList += [CRule(head, right)]

#--------------------------------------------------------------------------------------------------
def ContainRule(tree = CTree(), rDict = {}):
	rList = []
	ContainRuleHelper(tree, rDict, rList)

	return rList

#--------------------------------------------------------------------------------------------------
def ContainRuleHelper(tree = CTree(), rDict = {}, rList = []):
	if (tree.IsPreterminal() == True or tree.IsTerminal() == True):
		return None

	if (tree.GetVal() == None):
		if (tree.GetChildren() == None or len(tree.GetChildren()) == 0):
			return 
		else:
			tree = tree.GetChildren()[0]

	children = tree.GetChildren()
	(head ,right) = (tree.GetVal().split('_')[0], [])
	for child in children:
		ContainRuleHelper(child, rDict, rList)
		right += [child.GetVal().split('_')[0]]

	rule = CRule(head, right) 
	if rule in rDict:
		rList += [(tree,rule)]

#--------------------------------------------------------------------------------------------------

def CountRulesFromFile(path):
	fIn		= file(path)
	rDict	= {}
	for i,line in enumerate(fIn):
		if (i != 0 and i % 500 == 0):
			sys.stderr.write(str(i) + '\r')

		tree	= CTree.BuildTree(line.strip().decode('utf-8'))
		rules	= CollectRule(tree)

		for r in rules:
			if r in rDict:
				rDict[r] += 1
			else:
				rDict[r] = 1
	fIn.close()
	return rDict;

	
if (__name__ == '__main__'):
	
	verbose = True

	# collect rules from gold and auto-seged files
	rGoldDict = CountRulesFromFile('data\\all.chtrees.withid.gb.gold')
	rAutoDict = CountRulesFromFile('data\\auto.new.res')

	# find some wired rules
	rWiredUnaryDict = {}
	for r in rAutoDict:
		if r not in rGoldDict and r.IsUnary():
			rWiredUnaryDict[r] = rAutoDict[r]
	
	for r in rWiredUnaryDict.keys():
		if rWiredUnaryDict[r] > 0:
			print r.toString().encode('utf-8') + "   :   " + str(rWiredUnaryDict[r])
		else:
			del rWiredUnaryDict[r]
					
	print 'total %d unseen unary rules'% len(rWiredUnaryDict)

	fAuto		= file('data\\auto.new.res')
	fWiredTree	= file('data\\auto.wired.res.txt', 'w')
	for i, line in enumerate(fAuto):
		if (i != 0 and i % 500 == 0):
			sys.stderr.write(str(i) + '\r')

		tree			= CTree.BuildTree(line.strip().decode('utf-8'))
		containedRules	= ContainRule(tree, rWiredUnaryDict)
		
		if len(containedRules) != 0:
			fWiredTree.write('sentence ' + str(i + 1) + '\n')
			for (subTree, r) in containedRules:
				fWiredTree.write(r.toString().encode('utf-8') + '\n')
				subTree.GetParent().DisTreeStructure(fWiredTree)
				fWiredTree.write('\n\n')



	fAuto.close()
	fWiredTree.close()

