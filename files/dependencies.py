class dataClass(object):
	def __init__(self):
		self.data = []

	def enter(self, inputLine="> ", isFieldName=False):
		if not isFieldName:
			inp = trans(input(inputLine))
			self.data.append(inp)

		else:
			inp = input(inputLine)

			if inp.isidentifier():
				self.data.append(inp)

		return inp

def trans(string):
	for a in string:
		if not (a.isdigit() or a == "."):
			# If not a number
			return string

	return eval(string)

def createTableStruct():
	obj = dataClass()

	while True:
		field = obj.enter("Enter Field Name: ", True)

		if field.isidentifier():
			pass

		elif field == "":
			break

		else:
			print("*** INVALID FIELD NAME!! ***")

	f = open(db_filename, "ab")
	pickle.dump(obj, f)
	f.close()

	print("\nNOW YOU ARE ALL SET...\n")

def getFieldNames():
	f = open(db_filename, "rb")
	fieldNames = pickle.load(f).data
	f.close()
	return fieldNames

def tableAsMatrix():
	L = []
	f = open(db_filename, "rb")

	fieldNames = getFieldNames()

	try:
		while True:
			L.append(pickle.load(f))
	except: 
		f.close()

	for a in range(len(L)):
		L[a] = L[a].data

	return L

def CSV_as_matrix(csvList):
	List = []
	maxCols = len(csvList[0].split(","))

	for row in csvList:
		col = row.split(",")
		col = [x.strip() for x in col]

		if len(col) == maxCols:
			List.append(col)

	return List

def tabulate(tableMatrix, highlight_list=[]):
	""" Prints table based on tableMatrix.
		First row is considered to be field names.
	"""

	##  Some highlighting issues...

	fieldNames = tableMatrix[0]
	content = tableMatrix[1:]				# Remove field names from tableMatrix
	lenList = [len(str(a)) + 5 for a in fieldNames]

	if not highlight_list:
		highlight_list = [0 for a in tableMatrix]

	for row in tableMatrix:					# Read rows
		for colNum in range(len(lenList)):	# Read no. of cols :- TRAVERSE FIELDS
			if len(str(row[colNum])) > lenList[colNum]:
				lenList[colNum] = len(str(row[colNum]))


	# PRINT FIELDNAMES

	print()
	print("-" * (2 + sum(lenList) + 3 * len(fieldNames) - 1))			#########
	print("| ", end="")

	for a in range(len(lenList)):
		print("{:{}} | ".format(fieldNames[a], lenList[a]), end="")
	
	print()
	print("-" * (2 + sum(lenList) + 3 * len(fieldNames) - 1))

	# PRINT CONTENT

	for row in content:
		print("| ", end="")

		for colNum in range(len(lenList)):
			if colorSupport and highlight_list[colNum] == 1:
				print("\033[1;34m", end="")

			print("{:{}}".format(str(row[colNum]), lenList[colNum]), end="")

			if colorSupport:
				print("\033[0m", end="")

			print(" | ", end="")

		print()

	print("-" * (2 + sum(lenList) + 3 * len(fieldNames) - 1))
	print()

def invertListContent(bigList, smallList):
	return [x for x in bigList if x not in smallList]

def delMatrixCols(tableMatrix, col_idx_list):
	table = []
	rowList = []

	for a in tableMatrix:
		for b in range(len(a)):
			if b not in col_idx_list:
				rowList.append(a[b])

		table.append(rowList)
		rowList = []

	return table

def delCols(List_1D, col_idx_list):
	init_idx = [x for x in range(len(List_1D))]
	final_idx = invertListContent(init_idx, col_idx_list)

	final_list = [List_1D[x] for x in final_idx]

	return final_list

def findMatch(pattern, row, field_idx_list=None):
	""" Returns a list containing 1 (match found) or 0 (no match found) 
		or -1 (excluded from finding match) for that particular col in the row.
	"""

	result = []

	if not field_idx_list:
		field_idx_list = [x for x in range(len(row))]

	# Find full match

	for a in range(len(row)):
		if a in field_idx_list:
			reObj = re.fullmatch(pattern, str(row[a]), re.IGNORECASE)

			if reObj:
				result.append(1)
			else:
				result.append(0)

		else:
			result.append(-1)

	return result
