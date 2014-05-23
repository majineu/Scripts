from Tree import *

def RemovePOSHelper(tree, Puncs):
	verbose = False
	if tree == None:
		return None


	if tree.IsNonTerminal():
		Children = tree.GetChildren()
		
		if verbose:
			print 'before remove:'
			tree.DisTreeStructure(sys.stdout)
		
		Children = filter(lambda x: x.m_val not in Puncs, Children)
		if len(Children) == 0:
			return None

		Children = map(lambda x: RemovePOSHelper(x, Puncs), Children)
		Children = filter(lambda x: x is not None, Children)

		if len(Children) == 0:
			return None



#		for child in Children:
#			if child.m_children == None or len(child.m_children) == 0:
#				Children.remove(child)
		
		if verbose:
			print 'after remove:'
			tree.m_children = Children
			tree.DisTreeStructure(sys.stdout)
		
		tree.m_children = Children
	return tree



def RemovePunc(tree):
	""" remove punctions from the given constituent tree """
	verbose = False
	if verbose:
		print('before remove:')
		tree.DisTreeStructure(sys.stdout)

	puncs = [",", ".", ":", "``", "''", "-LRB-", "-RRB-", "PU"]
	RemovePOSHelper(tree, puncs)

	if verbose:
		print('\nafter remove:\n')
		tree.DisTreeStructure(sys.stdout)

	return tree



def usage(name = ''):
	sys.stderr.write('usage: PuncProcessor.py  rmPunc input output')



if __name__ == '__main__':
	if len(sys.argv) != 4:
		usage()
		exit(0)


	if sys.argv[1] == 'rmPunc':
		trees = CTree.ReadingTrees(sys.argv[2])
		trees = map(RemovePunc, trees)

		fOut = file(sys.argv[3], 'w')
		
		for i,tree in enumerate(trees):
			if tree is not None:
				if tree.m_val == 'ROOT':
					tree = tree.m_children[0]
				tree.PrintTree(fOut, True)
				fOut.write('\n')
			else:
				sys.stderr.write('sentence %d is none after remove punc\n' %i)
		
		fOut.close()
	else:
		usage(0)



	
	





