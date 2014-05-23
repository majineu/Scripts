from TreeClass import *

if (len(sys.argv) not in [3, 4]):
	print 'usage : python DepTreeDrawer.py inputFile outputFile (conll)'
	print 'note  : output file is in utf-8 encoding'
	sys.exit(0)

	
conllFormat = False
if (len(sys.argv) == 4):
	if (sys.argv[3] == 'conll'):
		conllFormat = True

fIn = file(sys.argv[1])
fOutTree = file(sys.argv[2], 'w')


tupleList = []
treeList  = []
treeNum = 0
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

for i, tree in enumerate(treeList):
	fOutTree.write('sentence %d\n' %(i+1))
	tree.PrintTree(0, 0, fOutTree)
	fOutTree.write('\n')
fIn.close()
fOutTree.close()
