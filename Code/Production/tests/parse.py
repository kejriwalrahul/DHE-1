import matplotlib.pyplot as plt

sizes = range(5, 21)

"""
f = open("errfile", "r")

times = []
for i, line in enumerate(f):
	if i%2 == 1:
		continue

	line = line[:line.index("user")]
	line = float(line)
	times.append(line)

print times
"""

times = [0.000101, 0.000192, 0.000274, 0.000216, 0.000311, 0.0006, 0.001059, 0.001765, 0.005207, 0.007553, 0.014357, 0.027721, 0.056316, 0.108517, 0.221218, 0.444569]

plt.plot(sizes, times)
plt.plot(sizes, times, 'ro')
plt.xlabel("log2 file size (in bytes)")
plt.ylabel("Time in seconds")
plt.show()