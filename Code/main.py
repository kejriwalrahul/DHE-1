# Custom Imports
from sbox import SBox
from ga import GeneticOptimization

# Python librart imports
import numpy as np

wh_matrix = None

def object_generator():
	global wh_matrix

	default_m = 6
	default_n = 4
	default_mapping = range(2**default_m)
	
	if wh_matrix == None:
		new_object = SBox(default_m, default_n, np.random.permutation(default_mapping))
		new_object.generate_wh()
		wh_matrix = new_object.wh_matrix
	else:
		new_object = SBox(default_m, default_n, np.random.permutation(default_mapping), wh_matrix)

	return new_object

"""
# 1. SBox equations
m = 4
n = 4

# 2. Generate Map
mapping = [0] * (2**m)

mapping[0] = 0xF
mapping[1] = 0x7
mapping[2] = 0xD
mapping[3] = 0x5
mapping[4] = 0x8
mapping[5] = 0x0
mapping[6] = 0xA
mapping[7] = 0x2
mapping[8] = 0xB
mapping[9] = 0x3
mapping[10] = 0x9
mapping[11] = 0x1
mapping[12] = 0xC
mapping[13] = 0x4
mapping[14] = 0x0
mapping[15] = 0xE


# 3. Generate Lat & Dat  
mysbox = SBox(m, n, mapping)
mysbox.tables()

# 4. Save lat to file
fil = open('Output/my_sbox_lat', 'w')
mysbox.write_lat_to_file(fil)
fil.close()

# 5. Save lat to file
fil = open('Output/my_sbox_dat', 'w')
mysbox.write_dat_to_file(fil)
fil.close()

print mysbox.non_linearity()
print mysbox.fitness()
"""

# 6. Run GA Optimization
ga = GeneticOptimization(SBox, object_generator)
best_arr = ga.run(16)
for best in best_arr:
	print "best: ", best.non_linearity()
	print "Valid: ", best.check_bijective()
	print best.S