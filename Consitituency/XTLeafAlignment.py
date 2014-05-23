from Tree import *
from Rule import *
import re

class CSpan:
	__slots__ = ('beg', 
				 'end')

	def __init__(self, b = 0, e = 0):
		self.beg = b
		self.end = e

	def __str__(self):
		return '(%d %d)' %(self.beg, self.end)

#--------------------------------------------------------------------------------------
def ProcessLostWord(terminalNodes = [], autoSegSen = u''):
	autoNoSeg = u''.join(autoSegSen.strip().split(u' '))
	i = 0
	while i < len(terminalNodes):
		node = terminalNodes[i]
		word = node.GetVal()
		(index, nMatch) = Locate(autoNoSeg, word.lower())
		autoNoSeg = autoNoSeg[nMatch:]
		if (index == -1 or nMatch == 0):
			node.SelfDelete()
		else:
			node.SetVal(word[index: index + nMatch])
			if (index + nMatch != len(word)):
				newNode = node.Copy_InsertNewTerminalToTree()
				newNode.SetVal(word[index + nMatch:])
				terminalNodes.insert(i + 1, newNode)
		i += 1


#--------------------------------------------------------------------------------------
def LoadFullEn():
	fFull		= file('XTAlignResource.txt')
	fullEns		= fFull.readline().strip().decode('utf-8')
	fFull.close()
	return fullEns

#--------------------------------------------------------------------------------------
def cmpEn(ch1 = u'', ch2 = u''):
	if (ch1 in fullEns and ch2 in fullEns):
		if ((fullEns.find(ch2) - fullEns.find(ch1)) % 26 == 0):
			return True
	return False

#--------------------------------------------------------------------------------------
def Locate(sen = u'', word = u''):
	(index, length)	= (word.lower().find(sen[0].lower()), 0)
	if index != -1:
		for ch in sen:
			if index + length == len(word) or ch != word[index + length] :
				break;
			length += 1
	
	return (index, length)

#--------------------------------------------------------------------------------------
def GetIdMapping(treeNodeList = []):
	(newId, idMap) = (0, [])
	for tree in treeNodeList:
		if (tree.IsTerminal() == False):
			val = tree.GetVal()
			(label, old_id) = (val.split(u'_')[0], val.split(u'_')[1])
			idMap += [str(newId) + u'_' + old_id]
			tree.SetVal(label + u'_' + str(newId))
			newId += 1

	return idMap

#--------------------------------------------------------------------------------------
def Aligning(goldTree, autoSeg):
	(verbose, tree) = (False, CTree.BuildTree(goldTree))
	
	if (tree == None):
		return None

	terminalNodes	= tree.GetTerminals()
	autoWords		= autoSeg.strip().split(u' ')


	# raw sentence without segmentation 
	senNoSeg		= u''.join(autoWords)
	goldSen			= u''.join(tree.GetTerminalYield())

	# where gold and auto contain different characters
	if (len(senNoSeg) != len(goldSen)):
		if (verbose == True):
			print senNoSeg.encode('gbk')
			print goldSen.encode('gbk')
			print u' '.join(tree.GetTerminalYield()).encode('gbk')
		ProcessLostWord(terminalNodes, autoSeg.lower())
	
		if (verbose == True):
			print u' '.join(tree.GetTerminalYield()).encode('gbk')
			print ''
				
		# reset terminal node list
		terminalNodes	= tree.GetTerminals()
		
	(goldSpans, autoSpans, index) = ([],[], 0)
	
	if (verbose == True):
		sys.stderr.write('\nauto seg:\n' + autoSeg.encode('gbk') + '\n')
		tree.DisTreeStructure(sys.stderr, 'gbk')
		sys.stderr.write('\nafter alignment\n')
	


	# get gold and auto segmentation spans
	for node in terminalNodes:
		word	= node.GetVal()
		goldSpans += [CSpan(index, index + len(word))]
		index += len(word)

	index = 0
	for word in autoWords:
		autoSpans += [CSpan(index, index + len(word))]
		index += len(word)

	if (verbose == True):
		for span in autoSpans:
			print str(span)
		print ''
		for span in goldSpans:
			print str(span)
		print ''

	i = 0
	for spanIndex, autoSpan in enumerate(autoSpans):
		if (verbose == True):
			print str(autoSpan) + '   ' + str(goldSpans[i])

		if (goldSpans[i].end > autoSpan.end):

			nextAutoSpan = autoSpans[spanIndex + 1]
			if (nextAutoSpan.end <= goldSpans[i].end):
				# gold: abcd,  auto: a bc d  
				# here we need to insert a new span for 'bc' and
			    # a corresopnding terminal node
				newSpan = CSpan(autoSpan.end, goldSpans[i].end) 
				goldSpans[i].end = autoSpan.end
				
				# insert after i
				goldSpans.insert(i + 1, newSpan)
				newTerminal = terminalNodes[i].Copy_InsertNewTerminalToTree()
				terminalNodes.insert(i + 1, newTerminal)
			
			else:
				if (verbose == True):
					print 'autoSpan.end %d' % (autoSpan.end)

				if (i == len(goldSpans) - 1):
					goldSpans += [CSpan(autoSpan.end, len(senNoSeg))]
					newTerminal = terminalNodes[i].Copy_InsertNewTerminalToTree()
					terminalNodes.insert(i, newTerminal)
				else:
					goldSpans[i + 1].beg	= autoSpan.end
				
				goldSpans[i].end	= autoSpan.end
			
			i += 1

			
			
		elif (goldSpans[i].end < autoSpan.end):
			start = i
			while (goldSpans[i + 1].end < autoSpan.end):
				# None denotes the corresponding terminal node will be deleted
				i += 1
				goldSpans[i] = None
				
			i = i + 1
			if (goldSpans[i].end == autoSpan.end):
				# the case where gold: ab i: cd,  auto: abcd,
				# thus, we delete goldSpan[i]
				goldSpans[i] = None
				i += 1
			else:
				# the case where
				# gold: ab  i: cd ...  auto: abc  ...
				goldSpans[i].beg	= autoSpan.end
			
			goldSpans[start].end	= autoSpan.end
		else:
			i += 1
	
			
	# re-allocate word for terminals and delete empty node from tree
	for i in range(0, len(terminalNodes), 1):
		if (goldSpans[i] == None):
			terminalNodes[i].SelfDelete()
		else:
			terminalNodes[i].m_val = senNoSeg[goldSpans[i].beg: goldSpans[i].end]

	if (verbose == True):
		tree.DisTreeStructure(sys.stderr, 'gbk')
	return tree






def fillSlot(senOri = '', senGen = '', words = []):
	oriNoSeg = u''.join(senOri.split(u' '))
	senGenUnseg	 = u''.join(senGen.split(u' '))
	subs = re.split(u'(\$number)|(\$date)',senGenUnseg)
	subs = filter(lambda x: x not in[u'$date', u'$number', None], subs)
	(start, fillIn) = (0, [])
	for subSen in subs:
		ind = oriNoSeg.find(subSen, start)
		if (ind > start):
			fillIn += [oriNoSeg[start: ind]]
		start = ind + len(subSen)

	for word in senGen.split(u' '):
		if (word[0] == u'$'):
			word = fillIn[0]
			fillIn = fillIn[1:]
		words += [word]



def DeGeneralize(goldPath, genPath):
	fGold = file(goldPath)
	fGen  = file(genPath)

	for lineNum, gold_gen in enumerate(zip(fGold, fGen)):
		if (lineNum == 0):
			continue
		words = []
		fillSlot(gold_gen[0].strip().decode('utf-8'), gold_gen[1].strip().decode('utf-8'), words)
		pass

def CoverNodeTest(tree = CTree()):
	terminals = tree.GetTerminals()
	if (tree.CoverNodes(terminals)):
		print 'Cover'
	else:
		print 'unConver'
	

	for index in range(2, len(terminals), 1):
		Parent = tree.GetCommonParent(terminals[index - 2:index])
		
		print 'node list:'
		for node in terminals[index - 2: index]:
			if (node != None):
				node.PrintTree()
				print ''
		if (Parent != None):
			Parent.PrintTree()
			print '\n'
#-------------------------------------------------------------------------------	
	
def SelfDeleteTest(tree = CTree()):
	terminals = tree.GetTerminals()
	if (tree.CoverNodes(terminals)):
		print 'Cover'
	else:
		print 'unConver'
	start = len(terminals)/2
	
	for index in range(0, len(terminals), 1):
		sys.stderr.write('Before delete ' + terminals[index].GetVal().encode('gbk') + ':\n')
		tree.DisTreeStructure(sys.stderr, 'gbk')
		parent = terminals[index].SelfDelete()
	
		sys.stderr.write('After delete ' + terminals[index].GetVal().encode('gbk') + ':\n')
		if (tree.IsEmptyTree() == True):
			sys.stderr.write('Empty tree')
		else:
			tree.DisTreeStructure(sys.stderr, 'gbk')
	print ''	
#---------------------------------------------------------------------------------------------------------



def Generalize(treePath, genSegFile, genTreePath, EnFile = False):
	fTree	= file(treePath)
	fGenSeg	= file(genSegFile)
	fGenTree= file(genTreePath, 'w')
	nFail	= 0
	for i, linePair in enumerate(zip(fTree, fGenSeg)):
		tree = CTree.BuildTree(linePair[0].strip().decode('utf-8'))
		genSegWords = linePair[1].strip().decode('utf-8').split(u' ')
		genSegWords = filter(lambda x : x != u'', genSegWords)
		terminals = tree.GetTerminals()
		
		if i > 0 and i % 200 == 0:
			sys.stderr.write('processing line %d ....\r' %i)

		if len(genSegWords) != len(terminals):
			sys.stderr.write(('Error: word number inconsistent %d %d %d\n' %(i, len(terminals), len(genSegWords))))
			nFail += 1
			print u' '.join(genSegWords).encode('gbk')
			print u' '.join(tree.GetTerminalYield()).encode('gbk')
			if len(terminals) < 10: exit(0)

		for (treeNode, genWord) in zip(terminals, genSegWords):
			treeNode.SetVal(genWord)

		tree.PrintTree(fGenTree, EnFile)
		fGenTree.write('\n')


	fGenTree.close()
	fTree.close()
	fGenSeg.close()


def AligningFiles(goldTreePath, autoSenPath, resPath = 'data\\alignRes.txt',  isEnFile = False):
	fGold = file(goldTreePath)
	fGen  = file(autoSenPath)
	fRes  = file(resPath, 'w')
	fTreeGold = file(resPath + '.gold.tree', 'w')
	fTreeAuto = file(resPath + '.auto.tree', 'w')
	fIdMap	  = file(resPath + '.idMap', 'w')
	nFailed = 0
	for lineNum, gold_gen in enumerate(zip(fGold, fGen)):
		tree = Aligning(gold_gen[0].strip().decode('utf-8'),  gold_gen[1].strip().decode('utf-8'))

		# remove wired unary rule
		PostProcess(tree)
		if tree.ContainSelfLoops():
			#print '\nbefore processing self-loop:'
			#tree.DisTreeStructure()	
		
			tree.RemoveSelfLoops()
		
			#print '\nafter processing self-loop:'
			#tree.DisTreeStructure()
		
		
		
		if  lineNum % 1000 == 0 and lineNum != 0:
			sys.stderr.write('processing line ' + str(lineNum) + ' ...\r')

		if (tree != None):
			
			# result tree and id map
			nodeList = tree.GetPreOrderTreeList()
			idMap = GetIdMapping(nodeList)
			fIdMap.write(u' '.join(idMap).encode('utf-8') + '\n')

			tree.PrintTree(fRes, isEnFile)
			
			# display tree structure for debuging purpose
			treeGold = CTree.BuildTree(gold_gen[0].strip().decode('utf-8'))
			fTreeGold.write('sentence %d\n' % (lineNum + 1))
			fTreeAuto.write('sentence %d\n' % (lineNum + 1))
			treeGold.DisTreeStructure(fTreeGold)
			tree.DisTreeStructure(fTreeAuto)
			
		else:
			nFailed += 1

		fRes.write('\n')

	sys.stderr.write('total %d Failed\n' %nFailed)
	fRes.close()
	fGen.close()
	fGold.close()
	fTreeGold.close()
	fTreeAuto.close()
	fIdMap.close()
#---------------------------------------------------------------------------------------------------------

r1 = CRule('NP', ['ADJP'])
r2 = CRule('VP', ['ADVP'])
r3 = CRule('NP', ['VP'])
rDict = {r1: 1, r2:2,r3:3}
def PostProcess(tree):
	treeRules = ContainRule(tree, rDict)
	if len(treeRules) == 0:
		return 

	verbose = False
	if (verbose == True):
			sys.stderr.write('before processing %s:\n' %treeRules[0][1].toString().encode('utf-8'))
			tree.DisTreeStructure()

	for treeRule in treeRules:
		
		if (rDict[treeRule[1]] == 3):
			# NP->VP , remove NP
			(parent, child)		= (treeRule[0].GetParent(), treeRule[0].GetChildren()[0])
			parent.m_children	= filter(lambda x: x!= treeRule[0], parent.m_children)
			parent.m_children	+= [child]
			child.m_parent		= parent

			# disconnect NP
			treeRule[0].m_parent	= None
			treeRule[0].m_children	= None

			if (verbose == True):
				sys.stderr.write('\n\nafter processing %s:\n' %treeRule[1].toString().encode('utf-8'))
				parent.DisTreeStructure()

		else:
			# NP->ADJP  or  VP->ADVP, remove ADJP or ADVP
			subTree = treeRule[0].GetChildren()[0]
			if (len(subTree.GetChildren()) == 1):
				(parent, child)		= (subTree.GetParent(), subTree.GetChildren()[0])
				parent.m_children	= [child]
				child.m_parent		= parent

				# modify POS tag
				if (child.GetVal().find('AD') != -1):
					child.SetVal('VA' + '_' + child.GetVal().split('_')[1])
				else:
					child.SetVal('NN' + '_' + child.GetVal().split('_')[1]) 


				(subTree.m_parent, subTree.m_children) = (None, None)
				#if (verbose == True):
				#	sys.stderr.write('\n\nafter processing %s:\n' %treeRule[1].toString().encode('utf-8'))
				#	parent.DisTreeStructure()

	if (verbose == True):
		sys.stderr.write('after processing %s:\n' %treeRules[0][1].toString().encode('utf-8'))
		tree.DisTreeStructure()
				
			

def usage():
	sys.stderr.write('usage: python XTLeafAlignment.py  alignWords  goldTreeFile  autoSegFile  resFile  (Eng)\n')
	sys.stderr.write('usage: python XTLeafAlignment.py  genTreeNode treeFile  GenSegFile  resFile (Eng)\n')
	sys.stderr.write('     : all files are in utf-8 format\n')



if (__name__ == '__main__'):
	if len(sys.argv) not in [5, 6]:
		usage()	
		sys.exit(0)

	if sys.argv[1] == 'alignWords':
		if len(sys.argv) == 6:
			AligningFiles(sys.argv[2], sys.argv[3], sys.argv[4], True)
		else:
			AligningFiles(sys.argv[2], sys.argv[3], sys.argv[4])
	elif sys.argv[1] == 'genTreeNode':
		if len(sys.argv) == 6:
			Generalize(sys.argv[2],  sys.argv[3],  sys.argv[4], True)
		else:
			Generalize(sys.argv[2],  sys.argv[3],  sys.argv[4])
	else:
		usage()
	
	#AligningFiles('data\\all.chtrees.withid.gb.gold', 'data\\auto.new.txt', 'data\\auto.new.res')
	
