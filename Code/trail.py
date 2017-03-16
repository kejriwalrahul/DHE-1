def find_trail(noOfRound,totalSbox):
	result = []
	sboxType = "spn"

	#sboxType = "spn"
	sbno, row, col = 1, 1, 1
	totalBias = 1.0
	lat = []
	biasCount = 1
	# seq = [1,2,4,8,16,32,64,128]
	# seq = [1,2,4,8]

	latsubtractor = 0x1 << (8 - 1)
	latdivider = 0x1 << 8
	#find first weak sbox
	for k in range(1,totalSbox+1):
		lat = getLat(k,sboxType)
		for i in range(1,len(lat)):
			for j in range(1,len(lat[i])):
			# for j in seq:
				if (abs(lat[row][col]-latsubtractor) < abs(lat[i][j]-latsubtractor)):
					row, col, sbno = i, j, k

	totalBias *= (abs(lat[row][col]-latsubtractor)/float(latdivider))
	prevType = sboxType
	data = [row,col,sbno,sboxType]
	#print data
	activeInput = inputToIndex([data],sboxType,True)
	activeOutput = inputToIndex([data],sboxType)
	result.append([activeInput,activeOutput])
	#print activeOutput
	outList = permute(activeOutput,sboxType)
	activeOuts = activeOutput
	
	for rno in range(2,noOfRound+1):
		data = []
		nextType = getType(rno)	#sbox type
		out = indicesToInputs(outList,prevType,nextType)
		
		for val in out:	#val = [inputsum,outputsum,sbox_no,sbox_type]
			biasCount += 1
			lat = getLat(val[2],nextType)
			row = val[0]
			col = 1

			# for j in seq:
			for j in range(1,len(lat[row])):
				if (abs(lat[row][col]-latsubtractor) < abs(lat[row][j]-latsubtractor)):
					col = j
			data.append([row,col,val[2],val[3]])
			totalBias *= (abs(lat[row][col]-latsubtractor)/float(latdivider))
		
		activeInput = inputToIndex(data,nextType,True)
		activeOutput = inputToIndex(data,nextType)
		
		if (prevType == "spn" and nextType != prevType):
			for x in range(0,len(activeOuts)):
				if (x <= 64):
					activeOutput.append(x)
				else:
					break
			activeOutput.sort()

		result.append([activeInput,activeOutput])
		outList = permute(activeOutput,nextType)
		prevType = nextType
		activeOuts = activeOutput

	totalBias *= (0x1 << (biasCount-1))
	print "net bias = ",totalBias
	return result

#returns permutation table
def getPermutationTable(stype):
	file = open("../Output/permutation.dat","r")
	if (stype == "fiestel"):
		file.readline()
	val = file.readline()
	tab = map(int, val.rstrip().split())
	file.close()
	return tab


def expansion(data):
	file = open("../Output/permutation.dat", "r")
	file.readline()
	file.readline()
	val = file.readline()
	val = map(int,val.split())
	out = []
	#print len(val)," val length"
	for x in data:
		temp = (x-1) / 48
		out.append(temp * 48 + val[(x-1)%48])
	file.close()
	return out

#returns lat
def getLat(sboxNo, sboxType):
	if (sboxType == "spn"):
		file = open("../Output/sbox_8x8."+str(sboxNo-1),"r")
		for _ in range(0,9):
			file.readline()
		lat = []
		for i in range(0,256):
			val = file.readline()
			lat.append(map(int,val.strip().rstrip(",").split(", ")))
		file.close()
		return lat
	else:
		file = open("../Output/sbox_6x4."+str(sboxNo-1),"r")
		for _ in range(0,9):
			file.readline()
		lat = []
		for i in range(0,64):
			val = file.readline()
			lat.append(map(int,val.strip().rstrip(",").split(", ")))
		file.close()
		return lat

#return the type of network in the given round
def getType(roundNo):
	return "spn"

def permute(indexList, rType):
	val = []
	outList = []
	if (rType == "spn"):
		permTable = getPermutationTable("spn")
		for x in indexList:
			outList.append(permTable[x-1])
	else:
		permTable = getPermutationTable("fiestel")
		for x in indexList:
			outList.append(permTable[x-1])
	outList.sort()
	return outList


#takes an input bit, sbox no. and sbox type
#convert it to index, and return the list containing the indices
def inputToIndex(data,rType,inputsum = False):
	iList = []
	multiplier = 0
	if (rType == "spn"):
		multiplier = 8
	elif (inputsum):
		multiplier = 6
	else:
		multiplier = 4


	index = 1
	if (inputsum):
		index = 0

	for row in data:	#row = [inputsum,outputsum,sboxno,sboxtype]
		pad = row[2] * multiplier
		val = row[index]
		for i in range(0,8):
			if (val % 2 == 1):
				iList.append(pad-i)
			val = val >> 1
	if (not inputsum and rType == "fiestel"):
		iList = expansion(iList)
	iList.sort()
	return iList

#convert list of indices to sbox inputs based on
#the type of sbox
def indicesToInputs(vals,fromType,toType):
	oList = []
	if (fromType != toType):
		vals = convertIndexTypes(vals,fromType,toType)

	if (toType == "spn"):
		sbno = ((vals[0]-1) / 8) + 1
		index = 0x1 << ((vals[0]+7) % 8)
		
		for x in range(1,len(vals)):
			temp = ((vals[x]-1)/8) + 1
			if (temp != sbno):
				oList.append([index,0,sbno,"spn"])
				index = 0x0
				sbno = temp
			index = index ^ (0x1 << ((vals[x]+7) % 8))
		oList.append([index,0,sbno,"spn"])

	else:
		sbno = ((vals[0]-1)/6) + 1
		index = 0x1 << ((vals[0]+5) % 6)
		for x in range(1,len(vals)):
			temp = ((vals[x]-1)/6) + 1
			if (temp != rno):
				oList.append([index,0,sbno,"fiestel"])
				sbno = temp
				index = 0
			index = index ^ (0x1 << ((vals[x]+5)%6))
		oList.append([index,0,sbno,"fiestel"])
	return oList

#convert from one type of indices to other
def convertIndexTypes(vals,fromType,toType):
	if (fromType == toType):
		return vals

	data = []
	if (fromType == "spn"):
		for x in vals:
			p = x - 64
			if (p > 0):
				data.append(p)
	else:
		for x in vals:
			data.append(x+64)
	return data

#run trails
rs = find_trail(20,16)
for x in rs:
	print x