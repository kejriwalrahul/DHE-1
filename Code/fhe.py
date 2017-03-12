"""
	Program To Model FHE-1 Cipher and provide functions for computation of weakest trails

	Written By Rahul Kejriwal
	Started on 12/3/16
"""

"""
	Static Cipher Class modelling one round of the dynamic cipher 
"""
class FHE_Round:

	"""
		Initializes current structure
	"""
	def __init__(self, round_pattern, exp, conf, perm):
		self.expansion 	= exp
		self.confusion 	= conf
		self.permutation= perm

		for sbox in self.confusion:
			sbox.gen_lat_table()
			sbox.gen_dat_table()

	"""
		Function returning expanded set of active bits
	"""
	def expand(self, ip_set):
		op_set = []
		for ip in ip_set:
			op_set += [i for i,x in enumerate(self.expansion) if x == ip]

		return op_set

	"""
		Function returning confusion a list of tuples ([confused bits, bias])
		The list elements correspond to different confusion possibilities having non-zero bias
	"""
	def confuse(self, ip_set):
		pass

	"""
		Function returning permuted set of active bits
	"""
	def permute(self, ip_set):
		op_set = []
		for ip in ip_set:
			op_set.append(self.permutation.index(ip))

		return op_set