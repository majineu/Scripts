import sys
import re

goldF = file(sys.argv[1])
predF = file(sys.argv[2])

for lines in zip(goldF, predF):
	gold, pred = lines[0].strip(), lines[1].strip()
	if len(gold) == 0:
		print ''
	else:
		sys.stdout.write(pred)
		if re.split('\s+', gold)[2] != re.split('\s+', pred)[2]:
			sys.stdout.write(('::::%s\n' %re.split('\s+', gold)[2]))
		else:
			sys.stdout.write('\n')
	
