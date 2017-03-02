from sbox import SBox
from ga import GeneticOptimization

# 1. SBox equations
m = 4
n = 4

# 2. Generate Map
mapping = [0] * (2**m)

mapping[0] = 0xE
mapping[1] = 0x4
mapping[2] = 0xD
mapping[3] = 0x1
mapping[4] = 0x2
mapping[5] = 0xF
mapping[6] = 0xB
mapping[7] = 0x8
mapping[8] = 0x3
mapping[9] = 0xA
mapping[10] = 0x6
mapping[11] = 0xC
mapping[12] = 0x5
mapping[13] = 0x9
mapping[14] = 0x0
mapping[15] = 0x7

# 3. Generate Lat & Dat  
SBox.initialize()
# print SBox.wh_matrix
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

mysbox.S = [2, 9, 3, 6, 15, 10, 14, 7, 12, 1, 11, 0, 5, 8, 4, 13]
print mysbox.non_linearity()
# print mysbox.fitness()

# # 6. Run GA Optimization
# ga = GeneticOptimization(SBox)
# best = ga.run()
# print "best: ", best.non_linearity()