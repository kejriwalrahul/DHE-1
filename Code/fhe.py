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
		
		self.confusion is a list of SBox objects
	"""
	def __init__(self, round_pattern, exp, conf, perm):
		self.expansion 	= exp
		self.confusion 	= conf
		self.permutation= perm

		self.no_of_sbox = len(self.confusion)

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
		Function returning confusion a list of tuples ([(confused bits, bias)]*self.no_of_sbox)
		The list elements correspond to different confusion possibilities having non-zero bias
	
		type = 'lat' for lat, 'dat' for dat
	"""
	def confuse(self, ip_set, trail_type):
		sbox_ip_size = self.confusion[0].m

		# Break activated ip bits into diff activated SBox ips 
		activated_ips = []
		for i in range(self.no_of_sbox):
			curr_activated_bits = 0
			
			for j in range(sbox_ip_size):
				curr_activated_bits *= 2
				if (i*sbox_ip_size + j) in ip_set:
					curr_activated_bits += 1 

			activated_ips.append(curr_activated_bits)

		# Determine confusion possibilities with non-zero bias
		confusion_possibilities = []
		for i in range(self.no_of_sbox):
			this_sbox = self.confusion[i] 
			this_sbox_possibilities = []
			
			if trail_type == 'lat':
				lat_row = this_sbox.lat[activated_ips[i]]
				for j, cell in enumerate(lat_row):
					if cell != this_sbox.no_of_possible_ips / 2:
						cell_bias = cell*1.0 / this_sbox.no_of_possible_ips - 0.5 
						this_sbox_possibilities.append( (j, cell_bias) )
			else:
				dat_row = this_sbox.lat[activated_ips[i]]
				for j, cell in enumerate(dat_row):
					if cell != 0:
						prop_ratio = cell*1.0 / this_sbox.no_of_possible_ips 
						this_sbox_possibilities.append( (j, prop_ratio) )				

			confusion_possibilities.append(this_sbox_possibilities)

		return confusion_possibilities


	"""
		Function returning permuted set of active bits
	"""
	def permute(self, ip_set):
		op_set = []
		for ip in ip_set:
			op_set.append(self.permutation.index(ip))

		return op_set