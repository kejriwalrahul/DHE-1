"""
	Program To Compute The Linear Approximation Table and Difference Distribution Table for a given S-Box

	Written By Rahul Kejriwal
	Started on 27/2/16
"""

import numpy as np

"""
	Class used for representing the sbox
"""
class SBox:

	"""
		Class Configuration Functions
		-----------------------------

		__init__()
		__getitem__()
	"""



	"""
		Store the sbox in internal representation
		
		m = # of ip bits in sbox 
		n = # of op bits in sbox 
	
		mapping = List of 2**m (rows) of form of op for the ith input
	"""
	def __init__(self, m, n, mapping):
		# Store sbox dimensions
		self.m = m
		self.n = n
		
		# Store size of domain-space of sbox
		self.no_of_possible_ips = 2**m
		self.no_of_possible_ops = 2**n

		# Compute and store # of possible ip and op subset selections
		self.no_of_ip_subsets = 2**m
		self.no_of_op_subsets = 2**n

		# Store mapping
		self.S = mapping

		# Initialize lat and dat tables
		self.lat = None
		self.dat = None

		# Build lat table
		self.gen_lat_table()
		self.gen_dat_table()


	"""
		Allows use of sbox object as a map from i to S(i)
	"""
	def __getitem__(self, i):
		return self.S[i]



	"""
		Helper Member Functions
		-----------------------

		xor_sum()
		zero_count_in_map()
		op_diff_counts()
	"""



	"""
		Gets xor sum of bits in num(should be of size max(m,n) bits)
	"""
	def xor_sum(self, num):
		xsum = 0

		for i in range(max(self.m, self.n)):
			xsum ^= 1 if ((2**i) & num) else 0

		return xsum


	"""
		Given ip_selector row_sel and op_selector col_sel
		Computes the # of 0's that appear in the XOR dot product truth table
	"""
	def zero_count_in_map(self, row_sel, col_sel):
		count = 0

		for i in range(self.no_of_possible_ips):
			active_ip = row_sel & i			
			active_op = col_sel & self[i]			

			xor_ip_op = active_ip ^ active_op
			count += int(not self.xor_sum(xor_ip_op))

		return count


	"""
		Given ip difference and op difference
		Computes the # of matches for the given sbox
	"""
	def op_diff_counts(self, ipdiff):
		counts = [0]*self.no_of_possible_ops

		for i in range(self.no_of_possible_ips):
			x    = i
			xbar = ipdiff ^ i
			
			opdiff = self[x] ^ self[xbar]
			counts[opdiff] += 1

		return counts



	"""
		Member Functions for generating tables
		--------------------------------------

		gen_lat_table()
		gen_dat_table()
	"""



	"""
		Generate the LAT for given sbox
	"""
	def gen_lat_table(self):	

		# Initialize counts
		self.lat = [None]*(self.no_of_ip_subsets)
		for i in range(self.no_of_ip_subsets):
			self.lat[i] = [0]*self.no_of_op_subsets

		for i in range(self.no_of_ip_subsets):
			for j in range(self.no_of_op_subsets):
				self.lat[i][j] = self.zero_count_in_map(i,j)


	"""
		Generates the DAT for given sbox
	"""
	def gen_dat_table(self):

		# Initialize counts
		self.dat = [None]*(self.no_of_ip_subsets)

		for i in range(self.no_of_ip_subsets):
			self.dat[i] = self.op_diff_counts(i)



	"""
		Member Functions for printing Ops to File
		-----------------------------------------

		write_to_file()
		write_lat_to_file()
		write_dat_to_file()

	"""


	"""
		Generic table writer
	"""
	def write_to_file(self, fil, table, xmax, ymax):
		for i in range(xmax):
			for j in range(ymax):
				fil.write('{:4d},'.format(table[i][j]))
			fil.write("\n")


	"""
		Write the lat table of the sbox to fil
	"""
	def write_lat_to_file(self, fil):
		self.write_to_file(fil, self.lat, self.no_of_ip_subsets, self.no_of_op_subsets)


	"""
		Write the dat table of the sbox to fil
	"""
	def write_dat_to_file(self, fil):
		self.write_to_file(fil, self.dat, self.no_of_ip_subsets, self.no_of_op_subsets)



	
	def nl(self, row, ip_bit):
		count = 0
		for i in range(len(row)):
			curr = -1 if (self[i] & (2**ip_bit)) else 1
			if curr != row[i]:
				count += 1

		return count

	
	# Computes non-linearity of given sbox
	def non_linearity(self):
		wh_matrix = np.zeros((1,1))
		wh_matrix[0][0] = 1 
		for i in range(self.m):
			wh_matrix_new = np.zeros( (len(wh_matrix)*2, len(wh_matrix)*2,) )
			
			wh_matrix_new[:len(wh_matrix), :len(wh_matrix)] =  wh_matrix[:,:]
			wh_matrix_new[:len(wh_matrix), len(wh_matrix):] =  wh_matrix[:,:]
			wh_matrix_new[len(wh_matrix):, :len(wh_matrix)] =  wh_matrix[:,:]
			wh_matrix_new[len(wh_matrix):, len(wh_matrix):] = -wh_matrix[:,:]

			wh_matrix = wh_matrix_new

		print wh_matrix

		non_linearity = []
		for i in range(self.n):
			min_dist = 2**self.m

			for j in range(self.no_of_ip_subsets):
				res = self.nl(wh_matrix[j], i)
				# print res
				if res < min_dist:
					min_dist = res
					
			non_linearity.append(min_dist)

		return non_linearity

	# fitness based on non_linearity only
	def fitness(self):
		arr = self.non_linearity()
		fit_val = 100*min(arr);
		for x in arr:
			fit_val += x
		return fit_val

	def mutate(self):
		m_sbox = Sbox(self.m, self.n, self.mapping)
		x = np.random.randint(0,len(self.mapping))
		y = np.random.randint(0,len(self.mapping))
		m_sbox.mapping[x], m_sbox.mapping[y] = y, x
		return m_sbox

	def randomize(self):

	@staticmethod
	def crossover(first, second):