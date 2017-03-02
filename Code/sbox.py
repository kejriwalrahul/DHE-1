"""
	Program To Compute The Linear Approximation Table and Difference Distribution Table for a given S-Box

	Written By Rahul Kejriwal
	Started on 27/2/16
"""

import numpy as np
import sys

"""
	Class used for representing the sbox
"""
class SBox:

	"""
		Store the sbox in internal representation
		
		m = # of ip bits in sbox 
		n = # of op bits in sbox 
	
		mapping = List of 2**m (rows) of form of op for the ith input
	"""
	def __init__(self, m, n, mapping, wh_matrix = None):
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
		self.S = list(mapping)

		# Initialize lat and dat tables
		self.lat = None
		self.dat = None	

		# Setup wh-matrix
		self.wh_matrix = wh_matrix

	"""
		Allows use of sbox object as a map from i to S(i)
	"""
	def __getitem__(self, i):
		return self.S[i]


	"""
		Generate cryptanalysis tables
	"""		
	def tables(self):
		self.gen_lat_table()
		self.gen_dat_table()


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


	"""
		Initialize wh matrix
	"""
	def generate_wh(self):
		# Compute wh_matrix	
		wh_matrix = np.zeros((1,1))
		wh_matrix[0][0] = 1 
		
		for i in range(self.m):
			wh_matrix_new = np.zeros( (len(wh_matrix)*2, len(wh_matrix)*2,) )
			
			size_of_matrix = len(wh_matrix) 
			wh_matrix_new[:size_of_matrix, :size_of_matrix] =  wh_matrix[:,:]
			wh_matrix_new[:size_of_matrix, size_of_matrix:] =  wh_matrix[:,:]
			wh_matrix_new[size_of_matrix:, :size_of_matrix] =  wh_matrix[:,:]
			wh_matrix_new[size_of_matrix:, size_of_matrix:] = -wh_matrix[:,:]

			wh_matrix = wh_matrix_new

		self.wh_matrix = wh_matrix


	"""
		Compute hamming wt wrt single linear function
	"""
	def nl(self, row, op_bit_selector):
		count = 0
		
		row_representation = []
		for i in range(len(row)):
			curr = -1 if (self.S[i] & (2**op_bit_selector)) else 1
			# row_representation.append(float(curr))
			if curr != row[i]:
				count += 1

		# print np.array(row_representation)

		return count

	def nexl(self, row, op_bit_selector):
		count = 0
		
		row_representation = []
		for i in range(len(row)):
			curr = -1 if (self.S[i] & (2**op_bit_selector)) else 1
			row_representation.append(float(curr))
			if curr != row[i]:
				count += 1

		print np.array(row_representation)
	
	"""
		Computes non-linearity of given sbox
	"""
	def non_linearity(self):

		if self.wh_matrix == None:
			self.generate_wh()

		print self.wh_matrix
		non_linearity = []
		# for i in range(self.n):
		for i in range(1):
			min_dist = 2**self.m

			for j in range(self.no_of_ip_subsets):
				res = self.nl(self.wh_matrix[j], i)
				# print res
				min_dist = min(min_dist, res)
					
			non_linearity.append(min_dist)
			self.nexl(self.wh_matrix[0],i)
		if 8 in non_linearity:
			print non_linearity
			print self.S
			sys.exit(0)
		return non_linearity


	#computes balanceness
	def balanceness(self):
		pass


	# get a exact copy
	def getCopy(self):
		new_sbox = SBox(self.m, self.n, self.S)
		return new_sbox


	# fitness based on non_linearity only
	def fitness(self):
		non_linearity = self.non_linearity()
		return 99 * min(non_linearity) + sum(non_linearity)


	# Returns mutated copy of self
	def mutate(self):
		m_sbox = self.getCopy()
		
		x = np.random.randint(0,len(self.S))
		y = np.random.randint(0,len(self.S))
		m_sbox.S[x], m_sbox.S[y] = m_sbox.S[y], m_sbox.S[x]

		return m_sbox


	#utility method for crossover
	def swapData(self,parent, pos):
		mem = set(self.S[:pos])
		
		j = 0
		for i in range(pos,len(self.S)):
			while (parent.S[j] in mem):
				j = j+1
			self.S[i] = parent.S[j]
			mem.add(parent.S[j])
			j = j+1


	#ordered crossover
	@staticmethod
	def crossover(first, second):
		child1 = first.getCopy()
		child2 = second.getCopy()

		pos = np.random.randint(1, len(first.S))
		child1.swapData(second,pos)
		child2.swapData(first,pos)
		
		return [child1, child2]


	"""
		Checks if a given sbox is bijective
	"""
	def check_bijective(self):
		sorted_map = sorted(self.S)
		return np.array_equal(sorted_map, np.array(range(self.no_of_ip_subsets)))