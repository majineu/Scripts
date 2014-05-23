from Tree import *
from CSigHanTrans import *


class CPOSMerger(object):
	"""description of class"""

	@staticmethod
	def LoadDict(dictPath):
		fIn = file(dictPath)
		Dict = {}
		for line in fIn:

			if line[0] == '#':
				continue
			line = line.strip()
			if len(line) != 0:
				Dict[line.decode('utf-8').split('\t')[0]] = line.decode('utf-8').split('\t')[1]


		fIn.close()
		return Dict
	
	@staticmethod
	def MergingPos(dictPath, inPath, outPath):
		dict = CPOSMerger.LoadDict(dictPath)

		fIn = file(inPath)
		fOut = file(outPath, 'w')
		for (i, line) in enumerate(fIn):
			if i != 0 and i % 5000 == 0:
				sys.stderr.write('processing line %d\r' %i)

			tree = CTree.BuildTree(line.strip().decode('utf-8'))
			CPOSMerger.MergingPosPerTree(tree, dict)
			
			tree.PrintTree(fOut)
			fOut.write('\n')

		fOut.close()
		fIn.close()

	@staticmethod
	def MergingPosPerTree(tree = CTree(), dict = {}):
		preterminals = tree.GetPreTerminals()
		for node in preterminals:
			if node.GetVal() in dict:
				node.SetVal(dict[node.GetVal()])
			elif node.GetVal()[0:2] in dict:
				node.SetVal(dict[node.GetVal()[0:2]])
		


def Preprocessing(dictPath, configFile, inPath, outPath):
	dict = CPOSMerger.LoadDict(dictPath)
	config = CPOSMerger.LoadDict(configFile)
	
	fIn = file(inPath)
	fOut = file(outPath + '_'.join(config.keys()), 'w')
	fOutLog = file(outPath + '_'.join(config.keys()) + '.log', 'w')

	for (i, line) in enumerate(fIn):
		if i != 0 and i % 5000 == 0:
			sys.stderr.write('processing line %d\r' %i)


		tree = CTree.BuildTree(line.strip().decode('utf-8'))
#		if len(tree.GetTerminals()) < 5:
#			continue

		tree.DisTreeStructure(fOutLog, 'utf-8')

		# v_12 -> v
		if u'rmNumber' in config:
			CSigHanTrans.RemoveNumber(tree)
		
		# NP[xx] -> NP
		if u'rmFunctional' in config:
			CSigHanTrans.RemoveFunctional(tree)
		
		if u'rmDeDi' in config:
			CSigHanTrans.RemoveDeDi(tree)

		if u'mergeNP' in config:
			CSigHanTrans.MergingNounPhrase(tree)

		if u'mergeVP' in config:
			CSigHanTrans.MergingVerbPhrase(tree)
		tree.RemoveSelfLoops()

		CPOSMerger.MergingPosPerTree(tree, dict)
		CSigHanTrans.AddNonterminalSig(tree)

		tree.DisTreeStructure(fOutLog, 'utf-8')
		tree.PrintTree(fOut)
		fOut.write('\n')
		fOutLog.write('\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\n')
		#tree.PrintTree(fOut)
		fOutLog.write('\n')
	
	fIn.close()
	fOut.close()
	fOutLog.close()

def usage():
	sys.stderr.write('usage: python CSigHanPreprocess.py  tagMap  configFile  inputFile  outputFile\n')


if __name__ == '__main__':

	if len(sys.argv) != 5:
		usage()
		sys.exit(0)

	Preprocessing(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

