def find_trail(noOfRound,totalSbox):
	result = []
	sboxType = "spn"
	sbno, row, col = 1, 1, 1

	#find first weak sbox
	for k in range(1,totalSbox+1):
		lat = getLat(k,sboxType)
		
		for i in range(1,len(lat)):
			for j in range(1,len(lat[i])):
				if (abs(lat[row][col]-8) < abs(lat[i][j]-8)):
					row, col, sbno = i, j, k

	prevType = sboxType
	data = [row,col,sbno,sboxType]
	activeInput = inputToIndex([data],sboxType,True)
	activeOutput = inputToIndex([data],sboxType)
	result.append([activeInput,activeOutput])
	outList = permute(activeOutput,sboxType)
	activeOuts = activeOutput
	
	for rno in range(2,noOfRound+1):
		data = []
		nextType = getType(rno)	#sbox type
		out = indicesToInputs(outList,prevType,nextType)
		
		for val in out:	#val = [inputsum,outputsum,sbox_no,sbox_type]
			lat = getLat(val[2],nextType)
			row = val[0]
			col = 1

			for j in range(1,len(lat[row])):
				if (abs(lat[row][col]-8) < abs(lat[row][j]-8)):
					col = j
			data.append([row,col,val[2],val[3]])
		
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
	return result

#returns permutation table
def getPermutationTable(stype):
	file = open("../Output/permutation.dat","r")
	if (stype == "fiestel"):
		file.readline()
	val = file.readline()
	tab = map(int, val.rstrip().split())
	return tab


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
		return lat
	else:
		file = open("../Output/sbox_6x4."+str(sboxNo-1),"r")
		for _ in range(0,9):
			file.readline()
		lat = []
		for i in range(0,64):
			val = file.readline()
			lat.append(map(int,val.strip().rstrip(",").split(", ")))

#return the type of network in the given round
def getType(roundNo):
	return "spn"

def permute(indexList, rType):
	val = []
	outList = []
	if (rType == "spn"):
		permTable = getPermutationTable("spn")
		for x in indexList:
			outList.append(permTable[x])
	else:
		permTable = getPermutationTable("fiestel")
		for x in indexList:
			outList.append(permTable[i])
	outList.sort()
	return outList


#takes an input bit, sbox no. and sbox type
#convert it to index, and return the list containing the indices
def inputToIndex(data,rType,inputsum = False):
	iList = []
	multiplier = 6
	if (rType == "spn"):
		multiplier = 8

	index = 1
	if (inputsum):
		index = 0

	for row in data:	#val = [inputsum,outputsum,sboxno,sboxtype]
		pad = row[2] * multiplier
		val = row[index]
		for i in range(1,9):
			if (val % 2 == 1):
				iList.append(pad-i)
			val = val >> 1
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
# rs = find_trail(4,16)
# for x in rs:
# 	print x