import sys
import os
import re

if __name__ == '__main__':
	if len(sys.argv) != 3:
		sys.stderr.write('usage: depEvaler.py  goldFile  testFile\n')
		exit(0)

	puncs = [",", ".", ":", "``", "''", "-LRB-", "-RRB-", "PU"]
	
	disThres = 12
	fGold = file(sys.argv[1])
	fTest = file(sys.argv[2])
	
	
	disGoldList = []
	disPredList = []
	disCorrList = []
	for i in range(0, 100, 1):
		disGoldList += [0]
		disPredList += [0]
		disCorrList += [0]
	
	totalW, corrW = 0, 0
	totalPunc, corrPunc = 0, 0

	widx = 0
	for i, linePair in enumerate(zip(fGold, fTest)):
		lineGold, lineGuess = linePair[0].strip(), linePair[1].strip()

		if len(lineGold) != 0:
			if len(lineGuess) == 0:
				sys.stderr.write('Error: files unmatch\n%s\n%s\n' %(lineGold, lineGuess))
				exit(0)

			widx += 1
			golds, tests = re.split(u'\s+', lineGold), re.split(u'\s+', lineGuess)

			if len(golds) != len(tests) or golds[0] != tests[0]:
				sys.stderr.write('Error: files unmatch, line %d\ngold: %s\ntest: %s\n' %(i, lineGold, lineGuess))

			if golds[1] in puncs:
				totalPunc += 1.0
				if golds[2] == tests[2]:
					corrPunc += 1.0
			else:
				totalW += 1.0
				
				disGold = int(golds[2]) - widx
				disPred = int(tests[2]) - widx
				
				if disGold < 0:
					disGold = -disGold
				if disPred < 0:
					disPred = -disPred
					 
				
				if disGold > disThres:
					disGold = disThres
				if disPred > disThres:
					disPred = disThres
					
				if int(golds[2]) != 0:
					disGoldList[disGold] += 1.0
				
				if int(tests[2]) != 0:
					disPredList[disPred] += 1.0
				
				if golds[2] == tests[2]:
					corrW += 1.0
					
					if int(tests[2]) != 0:
						disCorrList[disPred] += 1.0
		else:
			widx = 0

	sys.stderr.write('totalW: %-6d, corr: %d, acc: %.2f%%\n' %(totalW, corrW, 100.0 * corrW/totalW))
	sys.stderr.write('totalPunc: %-6d, corr: %d, acc: %.2f%%\n' %(totalPunc, corrPunc, 100.0 * corrPunc/totalPunc))

	
	fGold.close()
	fTest.close()

	
	for i in range(1, disThres + 1, 1):
		prec = 0.0
		if disPredList[i] > 0.0:
			prec = 100.0 * disCorrList[i] / disPredList[i]
		
		recall = 0.0
		if disGoldList[i] > 0.0:
			recall = 100.0 * disCorrList[i] / disGoldList[i]
		
		f1 = 0.0
		if prec + recall > 0.0:
			f1 = 2 * prec * recall/ (prec + recall) 
		sys.stderr.write('dis %-5d,   gold %-5d,  pred %-5d, %-5.2f%%,  %-5.2f%%,   prec %-5.2f%%,   rec %-5.2f%%,  f1 %-2.2f%%\n' \
		% (i, disGoldList[i], disPredList[i], 100.0 * disGoldList[i]/totalW,  100.0 * disPredList[i]/totalW, prec, recall, f1))

	
