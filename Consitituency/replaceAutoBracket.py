import re, sys

replaceList = [('(', '-lrb-'), (')', '-rrb-')]
fin = file(sys.argv[1])
fout = file(sys.argv[2], 'w')
sys.stderr.write('replace () to -xrb-...\n')
for line in fin:
	for item in replaceList:
		line = line.replace(item[0], item[1])

	fout.write(line)



fin.close()
fout.close()