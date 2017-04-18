import string
import random
import subprocess
import re

def gen_random_file(size):
	f = open("bin/testfile-" + str(size), "w")
	f.write(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size)))
	f.close()

errfile = open("errfile", "w")

times = []
sizes = [2**i for i in range(5, 21)]
for s in sizes:
	gen_random_file(s)
	time = subprocess.check_output(["time", "./bin/cbc_fhe", "-e", "bin/testfile-" + str(s), "-o", "outfile"], stderr=errfile)
	print float(time)
	times.append(float(time))

print times