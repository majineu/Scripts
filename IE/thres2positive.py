import sys
import re

def isFloat(val):
	try:
		float(val)
		return True
	except ValueError:
		return False


if __name__ == '__main__':

	if len(sys.argv) < 3 or isFloat(sys.argv[1]) == False or sys.argv[2] not in ['pos', 'neg']:
		sys.stderr.write('usage: xx.py < input  confidence_threshold  pos/neg > output\n')
		exit(0)

	thres, flag = float(sys.argv[1]), sys.argv[2]
	items, n = [], 0
	sys.stderr.write('confidence_threshold: %.2f,  flag: %s\n' %(thres, flag))
	
	for line in sys.stdin:
#		if len(line.strip()) == 0:
		if line.find('----') != -1:
			if len(items) != 0:
				score = float(items[10])
				if (flag == 'neg' and score > thres) or (flag == 'pos' and score < thres):
					items = []
					continue

				bA1, eA1 = int(items[4]), int(items[5])
				bR,  eR  = int(items[6]), int(items[7])
				bA2, eA2 = int(items[8]), int(items[9])

				sen = re.split('\s+', items[11])
				pos = re.split('\s+', items[12])
				chk = re.split('\s+', items[13])

				for i in range(bA1, eA1, 1):
					sys.stdout.write('%-10s %-10s %-10s %-10s %-10s\n' %(sen[i], sen[i].lower(), pos[i], chk[i], 'ENT'))
				
				for i in range(eA1, bA2, 1):
					sys.stdout.write('%-10s %-10s %-10s %-10s ' %(sen[i], sen[i].lower(), pos[i], chk[i]))
					
					if flag == 'pos':
						if i == bR:
							sys.stdout.write('B-REL\n')
						elif i > bR and i < eR:
							sys.stdout.write('I-REL\n')
						else:
							sys.stdout.write('O\n')
					else:
						sys.stdout.write('O\n');
				
				for i in range(bA2, eA2, 1):
					sys.stdout.write('%-10s %-10s %-10s %-10s %-10s\n' %(sen[i], sen[i].lower(), pos[i], chk[i], 'ENT'))

				sys.stdout.write('\n\n')
			items = []
			n += 1
		else:
			items += [line.strip()]
			
	sys.stdout.write('\n\n')
	sys.stderr.write('total %d records\n' %(n))
