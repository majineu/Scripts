from Tree import *
import re
class CSigHanTrans(object):
	"""description of class"""

	dots = [u'?',u'?']
	@staticmethod
	def ContainDot(uniVal = u''):
		contain0 = uniVal.find(CSigHanTrans.dots[0]) != -1 
		contain1 = CSigHanTrans.dots[1] in uniVal
		return contain0 or contain1


	@staticmethod
	def MergingNounPhrase(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			if node.IsNonTerminal() and CSigHanTrans.ContainDot(node.GetVal()) == False:
				if node.GetVal()[0].lower() == u'n':
					node.SetVal('NP')

	@staticmethod
	def MergingVerbPhrase(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			if node.IsNonTerminal() and CSigHanTrans.ContainDot(node.GetVal()) == False:
				if node.GetVal()[0].lower() == u'v':
					node.SetVal('VP')

	# v_12 -> v
	@staticmethod
	def RemoveNumber(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			if node.GetVal() != None:
				index = node.GetVal().find(u'_')
				if index != -1: node.SetVal(node.GetVal()[0:index])


	# NP[xx] -> NP
	@staticmethod
	def RemoveFunctional(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			if node.GetVal() != None:
				index = node.GetVal().find(u'[')
				if index != -1: node.SetVal(node.GetVal()[0:index])

	@staticmethod
	def AddNonterminalSig(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			if node.GetVal() != None and node.IsNonTerminal():
				node.SetVal(node.GetVal() + u'|||nonTerminal')
		
	@staticmethod
	def RemoveNonterminalSig(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			index = node.GetVal()(u'|||nonTerminal')
			if index != -1: node.SetVal(node.GetVal()[:index])

	@staticmethod
	def RemoveDeDi(tree = CTree()):
		nonterminals = tree.GetPreOrderTreeList()
		for node in nonterminals:
			label = node.GetVal()
			index = label.find(u'?')
			if index == -1: index = label.find(u'?')

			if index != -1:
				print label.encode('utf-8')
				if label[0] in [u'G',u'A', u'P',u'N',u'V',u'S',u'D']:
					node.SetVal(label[:index])
				else:
					node.SetVal(label[index + 1:])
				print node.GetVal().encode('utf-8')


	@staticmethod
	def Transformat(tree = CTree()):
		CSigHanTrans.RemoveNumber(tree)
		CSigHanTrans.RemoveFunctional(tree)
		CSigHanTrans.RemoveDeDi(tree)
		CSigHanTrans.MergingVerbPhrase(tree)
		CSigHanTrans.MergingNounPhrase(tree)


		




