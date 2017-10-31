#!/usr/bin/python3

import pickle
from random import randint
from subprocess import Popen
import os
import re

## Check for color support in command line

try:
	from colorama import init
	init()

	colorSupport = True
except:
	if os.name == "nt":			# If OS is 'Windows'
		colorSupport = False
	else:
		colorSupport = True

## Definitions

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

## Initialize neon file

db_filename = "new_table.neon"

try:
	f = open(db_filename, "rb")

except:
	f = open(db_filename, "wb")
	print("FILE '{}' CREATED SUCCESSFULLY!!\n".format(db_filename))

f.close()

# ------ MAIN ------

while True:
	print("Make a selection: ")
	print()
	print("1) Add a record")
	print("2) Delete a record")
	print("3) Edit a record")
	print("4) Overwrite the file")
	print("5) Display as table")
	print("6) Display as csv")
	print("7) Plot a Graph (BETA)")
	print("8) Find in table")
	print("9) Import CSV")
	print("10) Export As...")
	print("11) EXIT")
	print()

	sel = int(input("Selection: "))
	print()

	if sel == 1:
		f = open(db_filename, "rb")

		try:
			fileLen = len(f.read())

		except UnicodeDecodeError:
			fileLen = 1

		f.close()

		if fileLen != 0:
			f = open(db_filename, "ab")
			obj = dataClass()

			fieldNames = getFieldNames()

			for a in fieldNames:
				obj.enter("Enter {}: ".format(a))

			pickle.dump(obj, f)

			print("\nSUCCESSFULLY ADDED 1 RECORD...\n")

		else:
			print("Table structure not defined!\nGET STARTED...\n")
			createTableStruct()

		f.close()

	elif sel == 2:
		f = open(db_filename, "rb")

		try:
			fileLen = len(f.read())

		except UnicodeDecodeError:
			fileLen = 1

		f.close()

		if fileLen != 0:
			L = []
			f = open(db_filename, "rb")

			fieldNames = getFieldNames()

			try:
				while True:
					L.append(pickle.load(f))
			except: 
				f.close()

			for a in range(1, len(L)):
				print("\t{}) ".format(a), end="")

				for b in range(len(fieldNames)):
					print("{}, ".format(L[a].data[b]), end="")

				print()

			print()

			delRec = input("Enter record number to delete (0 to CANCEL): ")
			delRec = int(delRec) if str(delRec).isdigit() else delRec

			if delRec in range(1, len(L)):
				f = open(db_filename, "wb")

				for a in range(len(L)):
					if a == delRec:
						pass

					else:
						pickle.dump(L[a], f)

				f.close()
				print("\nSUCCESSFULLY DELETED 1 RECORD...\n")

			else:
				print("Operation Aborted...\n".upper())

		else:
			print("Table structure not defined!\nGET STARTED...\n")
			createTableStruct()

	elif sel == 3:
		f = open(db_filename, "rb")

		try:
			fileLen = len(f.read())

		except UnicodeDecodeError:
			fileLen = 1

		f.close()

		if fileLen != 0:
			L = []
			f = open(db_filename, "rb")

			fieldNames = getFieldNames()

			try:
				while True:
					L.append(pickle.load(f))
			except: 
				f.close()

			for a in range(1, len(L)):
				print("\t{}) ".format(a), end="")

				for b in range(len(fieldNames)):
					print("{}, ".format(L[a].data[b]), end="")

				print()

			print()

			editRec = input("Enter record number to edit (0 to CANCEL): ")
			editRec = int(editRec) if str(editRec).isdigit() else editRec
			print()

			if editRec in range(1, len(L) + 1):
				obj = dataClass()
				fieldNames = getFieldNames()

				for a in fieldNames:
					obj.enter("Enter {}: ".format(a))

				f = open(db_filename, "wb")

				headerObj = dataClass()
				headerObj.data = fieldNames
				pickle.dump(headerObj, f)

				for a in range(1, len(L)):
					if a == editRec:
						pickle.dump(obj, f)

					else:
						pickle.dump(L[a], f)

				f.close()
				print("\nSUCCESSFULLY EDITED 1 RECORD...\n")

			else:
				print("Operation Aborted...\n".upper())

		else:
			print("Table structure not defined!\nGET STARTED...\n")
			createTableStruct()

	elif sel == 4:
		try:
			if input("Are you really sure to overwrite the file? [y / n] ").lower() == "y":
				pass
			else:
				raise Exception

			f = open(db_filename, "wb")
			f.close()

			inp = input("\nCreate table Structure now [y / n]: ")
			print("-" * 15)
			print()

			if inp.lower() == "y":
				createTableStruct()

			inp = input("Start Quick Entry [y / n]: ")
			print("-" * 15)

			if inp.lower() == "y":
				fieldNames = getFieldNames()

				f = open(db_filename, "ab")

				for a in range(int(input("\nHow many Entries: "))):
					obj = dataClass()
					print()

					for a in fieldNames:
						obj.enter("Enter {}: ".format(a))

					pickle.dump(obj, f)
					f.flush()

				f.close()
				print()

		except Exception:
			print("Operation Aborted...\n".upper())
			print()

	elif sel == 5:

		tableMatrix = tableAsMatrix()
		tabulate(tableMatrix)

	elif sel == 6:
		print("=" * 40)
		print()

		L = []
		f = open(db_filename, "rb")

		fieldNames = getFieldNames()

		try:
			while True:
				L.append(pickle.load(f))
		except: 
			f.close()

		for a in L[1:]:
			for b in range(len(fieldNames)):
				print("{}".format(a.data[b]), end="")

				if b != len(fieldNames) - 1:
					print(", ", end="")

			print()

		print()
		print("=" * 40)
		print()

	elif sel == 7:
		print("=" * 40)
		print(">>> PLOT A GRAPH:")
		print()

		fieldNames = getFieldNames()
		tableList = tableAsMatrix()
		numberIndex = [a for a in range(len(tableList[0]))]	# Index of all fields

		# Generate field index of those field that can be considered as values(numeric).

		nonValueListIndex = []

		for a in tableList[1:]:
			for b in range(len(a)):
				if type(a[b]) not in [int, float]:
					if b not in nonValueListIndex:
						nonValueListIndex.append(b)

		# Index of those fields that can be considered as values.
		valueListIndex = invertListContent(numberIndex, nonValueListIndex)

		for a in range(len(valueListIndex)):
			print("{}) {}".format(a + 1, tableList[0][valueListIndex[a]]))

		print()

		# Index of the field opted as value by USER.
		valIndex = int(input("Select value field: ")) - 1
		valIndex = valueListIndex[valIndex]

		print("\nYou selected '{}'".format(tableList[0][valIndex]))

		# Index of those fields that can be considered as labels.
		labelListIndex = nonValueListIndex

		print("-" * 40)
		print()

		for a in range(len(labelListIndex)):
			print("{}) {}".format(a + 1, tableList[0][labelListIndex[a]]))

		print()

		# Index of the field opted as label by USER.
		labelIndex = int(input("Select label field: ")) - 1
		labelIndex = labelListIndex[labelIndex]

		print("\nYou selected '{}'".format(tableList[0][labelIndex]))

		print("-" * 40)
		print()

		# Traverse the table: Find max len of label Name
		#                   : Figure out no. of chars to be printed

		maxLabelLen = 0
		valueList = [row[valIndex] for row in tableList[1:]]
		labelList = [row[labelIndex] for row in tableList[1:]]
		maxVal = max(valueList)
		maxChar = 50
		charList = {}

		for row in tableList[1:]:
			if len(row[labelIndex]) > maxLabelLen:

				# Keep track of max len of Label Name.
				maxLabelLen = len(row[labelIndex])

		for a in range(len(valueList)):
			# Generate dict of no. of chars to be printed against each label.
			charList[labelList[a]] = int(round(valueList[a] * maxChar) / maxVal)

		# Graph Printing

		print("{0:{1}}   {2}".format(tableList[0][labelIndex].upper(), maxLabelLen, tableList[0][valIndex].upper()))
		print()

		for a in range(1, len(tableList)):
			labelName = tableList[a][labelIndex]

			if colorSupport:
				print("{0:{1}} | \033[{4}m{2}\033[0m {3}".format(str(labelName), maxLabelLen, " " * charList[labelName], valueList[a - 1], randint(41, 46)))

			else:
				print("{0:{1}} | {2} {3}".format(str(labelName), maxLabelLen, "*" * charList[labelName], valueList[a - 1]))

		print()
		print("=" * 40)
		print()

	elif sel == 8:
		print("=" * 40)
		print(">>> FIND IN TABLE:")
		print()

		table = tableAsMatrix()
		fieldNames = getFieldNames()
		pattern = input("Find (Regular Expression):\n")

		print("\nSelect Fields to find in:\n")

		for a in range(len(fieldNames)):
			print("{}) {}".format(a + 1, fieldNames[a]))

		print()

		field_idx_list = input("Field Selection (multiple): ")
		
		if field_idx_list:
			field_idx_list = field_idx_list.split()
			field_idx_list = [int(x) - 1 for x in field_idx_list]

		else:
			field_idx_list = [x for x in range(len(fieldNames))]

		## Find

		new_table = []

		for row in table[1:]:
			result = findMatch(pattern, row, field_idx_list)

			if 1 in result:
				new_table.append(row)

		if new_table:
			tabulate([fieldNames] + new_table, result)
		else:
			print("\n*** No match found ***")

		print()
		print("=" * 40)
		print()

	elif sel == 9:
		print("=" * 40)
		print(">>> IMPORT CSV:")
		csvFiles = []

		for a in os.listdir():
			if a.endswith(".csv"):
				csvFiles.append(a)

		print("\nSelect CSV to load:\n")

		for a in range(len(csvFiles)):
			print("{}) {}".format(a + 1, csvFiles[a]))

		csvFileIndex = int(input("\nSelection: ")) - 1

		print()
		print("-" * 40)

		if csvFileIndex in range(len(csvFiles)):
			targetFile = csvFiles[csvFileIndex]
			f = open(targetFile)

			print("\nWhat do you want to do...")
			print()
			print("1) Create new file")
			print("2) Overwrite existing file")

			inp = int(input("\nSelection: "))

			print()
			print("-" * 40)

			if inp == 1:
				newFileName = input("\nEnter a filename to proceed:\n")

				try:
					# Checks whether the file already exists.

					f1 = open(newFileName + ".neon")
					f1.close()

					# If file exists.

					inp = input("\nThe file '{}.neon' already exists. Do you want to override the file [y / n] : ".format(newFileName))

					if inp.lower() == "y":
						access = True
					else:
						access = False

				except:
					# If file dosen't exists: Safe to write data.
					access = True

				if not newFileName:

					# If filename is not provided.
					# Automatic file naming.

					num = 1
					targetFile = targetFile[:-len(".csv")]

					while True:
						try:
							newFileName = targetFile + "_{}".format(num)
							f1 = open(newFileName + ".neon")
							f1.close()
							num += 1

						except:
							break

				newFileName += ".neon"
				
				if access:
					f1 = open(newFileName, "wb")
					csvMatrix = CSV_as_matrix(f.readlines())
					obj = dataClass()

					for a in csvMatrix:
						obj.data = a
						pickle.dump(obj, f1)

					f1.close()
					
					print("\nCreated file '{}'".format(newFileName))
					print("Switching to '{}'".upper().format(newFileName))

					db_filename = newFileName
				
				else:
					print("\nOPERATION ABORTED.")

			elif inp == 2:
				inp = input("Are you really sure to overwrite the file? [y / n] ").lower()
				
				if inp == "y":
					f1 = open(db_filename, "wb")

					csvMatrix = CSV_as_matrix(f.readlines())
					obj = dataClass()

					for a in csvMatrix:
						obj.data = a
						pickle.dump(obj, f1)

					f1.close()

					print("\nImport Successful.")

				else:
					print("\nOPERATION ABORTED.")

		print()
		print("=" * 40)
		print()

	elif sel == 10:
		print("=" * 40)
		print(">>> EXPORT AS:")
		print()

		print("\t1) HTML (for use in webpages)")
		print("\t2) CSV (for use in Excel)")

		inp = input("\nSelection: ")
		inp = int(inp) if inp.isdigit() else inp

		if inp == 1:
			print()
			print("-" * 40)
			print("> Export as HTML\n")

			htmlFilename = input("Enter a filename to save:\n") + ".html"
			caption = input("\nCaption: ")
			tableList = tableAsMatrix()
			fieldNames = getFieldNames()
			access = True

			print()

			try:
				f = open(htmlFilename, "r")
				f.close()

				inp = input("The file '{}' already exists. Do you want to override the file [y / n] : ".format(htmlFilename))

				if inp.lower() == "y":
					access = True
				else:
					access = False
					print("\nOperation Aborted.")

			except:
				pass

			if access:
				try:
					f = open(htmlFilename, "w")

				except:
					f = open(htmlFilename, "a")
					
				# f.writelines(["<body>", "\t<tbody>", "\t\t<font face = \"Open Sans\">", "\t\t<table style = \"color: #3F51B5;\" bordercolor = \"#000000\">"])

				f.writelines(

["""
<!DOCTYPE html>
<html>
<head>
<style>
	body {
		font-family: \"Open Sans\", \"Roboto\", \"Segoe UI\", \"Source Code Pro\", \"Calibri\";
	}
	table {
		border-collapse: collapse;
		width: 100%;
	}

	th, td {
		text-align: left;
		padding: 8px;
	}

	tr:nth-child(odd){background-color: #f2f2f2}

	th {
		background-color: #4CAF50;
		color: white;
	}
</style>
</head>
<body>

<h2>""" + caption + """</h2>

<table>
<tbody>
"""]
				)

				# f.writelines(["\t<tr>\n", "\t\t<th></th>\n"])

				f.writelines(["\t<tr>\n"])

				for a in fieldNames:
					f.writelines(["\t\t<th><b>{}</b></th>\n".format(a)])

				f.writelines(["\t</tr>\n"])

				for row in tableList[1:]:
					# f.writelines(["\t<tr>\n", "\t\t<td><b>{}</b></td>\n".format()])

					f.writelines(["\t<tr>\n"])

					for col in range(len(row)):
						f.writelines(["\t\t<td>{}</td>\n".format(row[col])])

					f.writelines(["\t</tr>\n"])

				f.writelines(

				["""
</tbody>
</table>

</body>
</html>
				"""]
				)

				f.close()

				print("SUCCESSFULLY EXPORTED AS HTML...")
				print("\nSaved '{}'".format(htmlFilename))
				
				try:
					Popen(r'explorer /select,' + htmlFilename)
				except Exception as e:
					print("[Failed opening Window: {}]".format(e))

		elif inp == 2:
			print()
			print("-" * 40)
			print("> Export as CSV\n")

			csvFilename = input("\nEnter a filename to save:\n") + ".csv"
			tableList = tableAsMatrix()
			access = True

			print()

			try:
				f = open(csvFilename, "r")
				f.close()

				inp = input("The file '{}' already exists. Do you want to override the file [y / n] : ".format(csvFilename))

				if inp.lower() == "y":
					access = True
				else:
					access = False
					print("\nOperation Aborted.")

			except:
				pass

			if access:
				f = open(csvFilename, "w")

				for row in tableList:
					for col in range(len(row)):
						f.write("{}".format(row[col]))

						if col != len(row) - 1:
							f.write(", ")

					f.write("\n")
				f.write("\n")

				f.close()

				print("SUCCESSFULLY EXPORTED AS CSV...")
				print("\nSaved '{}'".format(csvFilename))

				try:
					Popen(r'explorer /select,' + csvFilename)
				except Exception as e:
					print("[Failed opening Window: {}]".format(e))

		print("=" * 40)
		print()

	elif sel == 11:
		print("-" * 20 + "x" + "-" * 20)
		print()
		break