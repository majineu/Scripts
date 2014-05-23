from Tree import *

def usage():
	sys.stderr.write('usage: python ConstituentTree.py  disTree brFile  treeFile\n')
	sys.stderr.write('     : python ConstituentTree.py  goldBkl inFile outFile\n')



def toBerkelyGoldTagFormat(inPath, outPath = ''):
	treeList = CTree.ReadingTrees(inPath)
	fOut = file(outPath, 'w')
	for tree in treeList:
		wts = tree.GetTagWordList()
		outList = [item[0] + u'\t' + item[1] + u'-xx' for item in wts]
		fOut.write((u'\n'.join(outList)).encode('utf-8') + '\n\n')

	fOut.close()




if __name__ == '__main__':
	if len(sys.argv) not in [3, 4]:
		usage()
		sys.exit(0)

	sys.argv = sys.argv[1:]
	if len(sys.argv) == 3 and sys.argv[0] == 'disTree':
		fIn		  = file(sys.argv[1])
		fOut	  = file(sys.argv[2], 'w')
		for i,line in enumerate(fIn.readlines()):
			if (i != 0 and i % 2000 == 0):
				sys.stderr.write(str(i) + '\r')
			line	= line.strip().decode('utf-8')
			tree	= CTree.BuildTree(line)
			fOut.write('sentence %d\n' %(i+1))
			tree.DisTreeStructure(fOut, 'utf-8')
		
		fOut.close()
		fIn.close()
	elif len(sys.argv) == 3 and sys.argv[0] == 'goldBkl':
		toBerkelyGoldTagFormat(sys.argv[2], sys.argv[3])
	else:
		usage()



