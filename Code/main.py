# Custom Imports
from sbox import SBox
# from ga import GeneticOptimization

# Python librart imports
import numpy as np
"""
wh_matrix = None

def object_generator():
	global wh_matrix

	default_m = 6
	default_n = 4
	default_mapping = range(2**default_m)
	
	if wh_matrix is None:
		new_object = SBox(default_m, default_n, np.random.permutation(default_mapping))
		new_object.generate_wh()
		wh_matrix = new_object.wh_matrix
	else:
		new_object = SBox(default_m, default_n, np.random.permutation(default_mapping), wh_matrix)

	return new_object


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

"""
def modval(x):
	return x % 16
# 3. Generate Lat & Dat
temp = [
	[42, 20, 2, 3, 58, 15, 12, 6, 38, 57, 27, 21, 1, 59, 0, 49, 25, 28, 8, 14, 62, 63, 40, 43, 50, 26, 33, 54, 44, 29, 56, 18, 48, 35, 11, 32, 41, 39, 10, 55, 60, 17, 51, 19, 13, 52, 7, 9, 23, 30, 5, 46, 31, 34, 24, 45, 4, 36, 61, 47, 37, 16, 22, 53],
	[51, 24, 49, 17, 15, 10, 47, 29, 9, 59, 63, 21, 38, 46, 54, 44, 22, 1, 5, 37, 55, 43, 30, 48, 56, 6, 34, 60, 4, 26, 36, 3, 33, 19, 20, 0, 2, 58, 35, 42, 40, 23, 16, 13, 31, 12, 7, 61, 11, 18, 50, 41, 53, 39, 25, 52, 8, 57, 62, 28, 27, 32, 14, 45],
	[52, 36, 4, 20, 18, 39, 57, 43, 23, 60, 21, 27, 49, 17, 45, 7, 47, 16, 22, 62, 13, 34, 51, 14, 40, 58, 38, 44, 9, 42, 11, 2, 15, 48, 28, 1, 56, 31, 53, 12, 41, 54, 24, 10, 29, 59, 63, 46, 5, 37, 55, 30, 6, 26, 3, 33, 19, 61, 0, 32, 8, 50, 35, 25],
	[55, 29, 10, 44, 7, 26, 22, 54, 6, 31, 39, 58, 11, 30, 0, 18, 34, 19, 15, 52, 43, 45, 8, 28, 38, 56, 57, 24, 49, 17, 47, 9, 59, 63, 21, 46, 1, 35, 41, 14, 51, 12, 60, 4, 25, 62, 48, 53, 36, 40, 13, 3, 23, 32, 5, 20, 37, 42, 16, 2, 27, 33, 50, 61],
	[51, 24, 49, 17, 15, 10, 47, 29, 9, 59, 63, 21, 38, 46, 54, 44, 61, 1, 5, 37, 55, 43, 30, 48, 56, 6, 34, 60, 4, 26, 36, 3, 33, 19, 20, 0, 2, 58, 35, 42, 40, 23, 16, 13, 31, 12, 7, 22, 11, 18, 50, 41, 53, 39, 25, 52, 8, 57, 62, 14, 28, 32, 45, 27],
	[40, 0, 54, 14, 42, 25, 36, 9, 57, 4, 2, 59, 37, 33, 24, 46, 43, 1, 5, 47, 55, 11, 35, 56, 50, 34, 61, 60, 16, 3, 30, 39, 51, 15, 32, 58, 7, 31, 23, 38, 17, 26, 6, 8, 48, 20, 27, 29, 49, 18, 10, 19, 44, 21, 41, 28, 13, 22, 52, 63, 53, 45, 12, 62],
	[51, 24, 49, 17, 15, 10, 47, 29, 9, 59, 63, 21, 38, 46, 28, 44, 22, 1, 5, 37, 55, 43, 30, 48, 56, 6, 34, 60, 4, 26, 36, 3, 33, 19, 20, 2, 61, 14, 16, 0, 41, 58, 32, 53, 8, 50, 18, 57, 31, 52, 39, 23, 27, 45, 7, 62, 13, 54, 40, 35, 12, 25, 11, 42],
	[52, 36, 4, 20, 18, 47, 57, 43, 23, 60, 21, 27, 49, 17, 45, 31, 39, 16, 22, 62, 13, 34, 51, 14, 40, 58, 38, 44, 9, 42, 11, 2, 15, 48, 28, 1, 56, 7, 53, 12, 41, 54, 24, 10, 29, 59, 63, 46, 5, 37, 55, 30, 6, 26, 3, 33, 19, 61, 50, 25, 0, 35, 8, 32],
	[42, 20, 2, 3, 58, 15, 12, 6, 38, 57, 27, 21, 1, 59, 0, 49, 25, 28, 8, 14, 62, 63, 40, 43, 50, 26, 33, 54, 44, 46, 56, 18, 48, 35, 11, 32, 41, 47, 10, 39, 60, 17, 51, 19, 13, 52, 7, 9, 23, 4, 29, 22, 31, 30, 34, 24, 5, 37, 55, 36, 16, 61, 45, 53],
	[4, 29, 10, 44, 7, 26, 22, 54, 6, 31, 39, 58, 11, 30, 0, 18, 34, 19, 15, 52, 43, 45, 8, 28, 38, 56, 51, 24, 49, 17, 47, 9, 59, 63, 21, 46, 1, 35, 41, 14, 57, 12, 60, 55, 25, 62, 48, 53, 36, 40, 13, 3, 23, 32, 37, 5, 61, 20, 2, 16, 27, 50, 33, 42],
	[42, 20, 2, 3, 58, 15, 12, 6, 38, 57, 27, 21, 1, 59, 0, 49, 25, 28, 8, 14, 62, 63, 40, 43, 50, 26, 17, 54, 44, 46, 56, 18, 48, 35, 11, 32, 41, 39, 10, 55, 60, 33, 51, 19, 13, 52, 7, 9, 23, 47, 36, 4, 45, 16, 22, 34, 37, 31, 30, 24, 29, 53, 61, 5],
	[51, 24, 49, 17, 15, 10, 47, 29, 9, 59, 63, 21, 38, 46, 54, 14, 61, 1, 5, 20, 55, 43, 30, 48, 56, 6, 34, 60, 4, 26, 36, 3, 33, 19, 37, 0, 2, 58, 35, 42, 40, 23, 16, 13, 57, 12, 7, 22, 11, 18, 50, 31, 41, 44, 53, 39, 25, 52, 8, 62, 28, 32, 45, 27],
	[31, 57, 27, 28, 11, 32, 41, 21, 40, 39, 42, 10, 35, 54, 47, 60, 17, 20, 6, 51, 19, 58, 44, 13, 56, 50, 23, 1, 2, 36, 0, 30, 5, 38, 15, 53, 24, 34, 45, 14, 29, 25, 8, 52, 4, 18, 43, 49, 7, 16, 62, 12, 9, 48, 22, 59, 63, 46, 37, 55, 26, 3, 33, 61],
	[3, 35, 20, 48, 54, 28, 63, 9, 12, 16, 23, 34, 57, 43, 32, 2, 52, 24, 46, 44, 59, 38, 62, 37, 25, 21, 40, 17, 0, 49, 53, 4, 41, 50, 1, 26, 42, 39, 6, 18, 27, 51, 36, 19, 5, 22, 58, 61, 55, 33, 45, 60, 47, 8, 13, 11, 31, 30, 14, 29, 56, 10, 7, 15],
	[52, 36, 4, 20, 18, 47, 57, 43, 23, 60, 21, 27, 49, 17, 45, 31, 39, 16, 22, 62, 13, 34, 51, 14, 40, 58, 38, 44, 9, 41, 11, 2, 15, 48, 28, 1, 25, 7, 53, 12, 42, 54, 24, 10, 29, 59, 63, 46, 5, 37, 55, 30, 50, 33, 26, 6, 0, 19, 8, 61, 3, 56, 32, 35],
	[42, 20, 2, 3, 58, 15, 12, 6, 38, 57, 27, 21, 1, 59, 0, 49, 25, 28, 8, 14, 62, 63, 40, 43, 50, 26, 33, 54, 44, 46, 56, 18, 48, 35, 11, 32, 41, 39, 10, 47, 52, 36, 4, 23, 60, 17, 45, 7, 16, 22, 13, 34, 51, 61, 53, 31, 30, 9, 5, 19, 24, 37, 55, 29]
]

for tabNo in range(16):
	mapping = map(modval,temp[tabNo])
	mysbox = SBox(6, 4, mapping)
	mysbox.generate_wh()
	# print mysbox.wh_matrix
	mysbox.tables()
	# 4. Save lat to file
	fil = open('Output/sbox_6x4.'+str(tabNo), 'w')
	fil.write("Type: 6x4\n\n")
	fil.write("Mapping: ")
	fil.write(str(mapping))
	fil.write("\n\nBalanceness: ")
	fil.write(str(mysbox.balanceness()))
	fil.write("\n\nNon-linearity: ")
	fil.write(str(mysbox.non_linearity()))
	fil.write("\n\nLAT Table:\n")
	vals = mysbox.write_lat_to_file(fil)
	bias = max(abs(32-vals[0]),abs(32-vals[1])) / 64.0
	fil.write("\nBias: "+str(bias))
	fil.close()

	# 5. Save lat to file
	fil = open('Output/sbox_6x4.'+str(tabNo), 'a')
	fil.write("\n\nDAT Table:\n")
	mysbox.write_dat_to_file(fil)
	fil.close()

# print mysbox.non_linearity()
# print mysbox.fitness()


# # 6. Run GA Optimization
# ga = GeneticOptimization(SBox, object_generator)
# best_arr = ga.run(16, 'pop_file')
# for best in best_arr:
# 	print "best: ", best.non_linearity()
# 	print "Valid: ", best.check_bijective()
# 	print best.S
