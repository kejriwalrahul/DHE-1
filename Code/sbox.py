"""
	Program To Compute The Linear Approximation Table and Difference Distribution Table for a given S-Box

	Written By Rahul Kejriwal
	Started on 27/2/16
"""


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

		for i in range(0, self.no_of_possible_ips):
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

		for i in range(0, self.no_of_ip_subsets):
			for j in range(0, self.no_of_op_subsets):
				self.lat[i][j] = self.zero_count_in_map(i,j)

	"""
		Generates the DAT for given sbox
	"""
	def gen_dat_table(self):
		# Initialize counts
		self.dat = [None]*(self.no_of_ip_subsets)

		for i in range(0, self.no_of_ip_subsets):
			self.dat[i] = self.op_diff_counts(i)

	"""
		Write the lat table of the sbox to fil
	"""
	def write_lat_to_file(self, fil):
		for i in range(0, self.no_of_ip_subsets):
			for j in range(0, self.no_of_op_subsets):
				fil.write('{:4d},'.format(self.lat[i][j]))
			fil.write("\n")

	"""
		Write the dat table of the sbox to fil
	"""
	def write_dat_to_file(self, fil):
		for i in range(0, self.no_of_ip_subsets):
			for j in range(0, self.no_of_op_subsets):
				
				fil.write('{:4d},'.format(self.dat[i][j]))
			fil.write("\n")
