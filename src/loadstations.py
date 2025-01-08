import sys
import subprocess

for line in sys.stdin:
	line2 = line.rstrip().split()
	subprocess.call(['mpc', 'add', line2[1]])
