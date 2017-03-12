def find_trail(noOfRound,totalSbox):
	result = []
	sboxType = "spn"
	sbno, row, col = 1, 1, 1

	#find first weak sbox
	for k in range(1,totalSbox+1):
		lat = getLat(k,sboxType)
		
		for i in range(1,len(lat)):
			for j in range(1,lat[i]):
				if (abs(lat[row][col]-8) < abs(lat[i][j]-8)):
					row, col, sbno = i, j, k

	prevType = sboxType
	data = [row,col,sbno,sboxType]
	activeInput = inputToIndex(data[0],data[2],sboxType)
	activeOutput = inputToIndex(data[1],data[2],sboxType)
	result.append([activeInput,activeOutput])
	outList = permute(activeOutput,sboxType)
	
	for rno in range(2,noOfRound+1):
		data = []
		nextType = getType(rno)	#sbox type
		out = indicesToInputs(outList,prevType,nextType)
		
		for val in out:	#val = [inputsum,outputsum,sbox_no,sbox_type]
			lat = getLat(val[2],nextType)
			row = val[0]
			col = 1

			for j in range(1,lat[row]):
				if (abs(lat[row][col]-8) < abs(lat[row][j]-8)):
					col = j
		
		activeInput = inputToIndex(data[0],data[2],nextType)
		activeOutput = inputToIndex(data[1],data[2],nextType)
		result.append([activeInput,activeOutput])
		outList = permute(activeOutput,nextType)
		prevType = nextType
	return result

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
	outList = sort(outList)
	return outList


#takes an input bit, sbox no. and sbox type
#convert it to index, and return the list containing the indices
def inputToIndex(val,sbno,rType):
	iList = []
	pad = 0
	if (rType == "spn"):
		pad = (sbno)*8
	else:
		pad = (sbno)*6

	for i in range(1,9):
		if (val % 2 == 1):
			iList.append(pad-i)
		val = val >> 1
	return iList

#convert list of indices to sbox inputs based on
#the type of sbox
def indicesToInputs(vals,fromType,toType):
	oList = []
	if (fromType != toType):
		vals = convertIndexTypes(vals,fromType,toType)

	if (toType == "spn"):
		rno = (vals[0] / 8) + 1
		index = (vals[0]+7) % 8
		for x in range(1,len(vals)):
			temp = (x/8) + 1
			if (temp != rno):
				oList.append([index,0,rno,"spn"])
			else:
				index = index ^ ((val[x]+7) % 8)
		oList.append([index,0,rno,"spn"])

	else:
		rno = (vals[0]/6) + 1
		index = (vals[0]+5) % 6
		for x in range(1,len(vals)):
			temp = (x/6) + 1
			if (temp != rno):
				oList.append([index,0,rno,"fiestel"])
			else:
				index = index ^ ((val[x]+5)%6)
		oList.append([index,0,rno,"fiestel"])
	return oList

#convert from one type of indices to other
def convertIndexTypes(vals,fromType,toType):
	if (fromType == toType):
		return vals

	data = []
	if (fromType == "spn"):
		for x in vals:
			p = x - 64
			if (p > 0)
				data.append(p)
	else:
		for x in vals:
			data.append(x+64)
	return data