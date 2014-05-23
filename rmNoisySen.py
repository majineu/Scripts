import sys
rm = 0
if len(sys.argv) != 2:
	sys.stderr.write('\nusage: xx.py rate < input > output\n\n')
	exit(0)

rate = float(sys.argv[1])
log = file('log', 'w')
sys.stderr.write('alpha ratio %.2f\n'%rate)
for i, line in enumerate(sys.stdin):
	if i % 100000 == 0:
		sys.stderr.write('processing %d line\r' %i)

	line = line.strip()	
	total, alpha = 0, 0
	for ch in line:
		if ch.isalpha():
			total += 1
			alpha += 1
		elif ch != ' ':
			total += 1

	if 1.0 * alpha/total > rate:
		sys.stdout.write(line + '\n')
	else:
		rm+=1
		log.write('%-5d %-5d' %(total - alpha, total))
		log.write(line + '\n')
log.close()
sys.stderr.write('total %d out of %d,  %.2f%% sentences removed\n' %(rm, i, 100.0*rm/i))
