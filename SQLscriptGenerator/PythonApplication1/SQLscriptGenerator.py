
translationfilename = "../translation.txt"
SQLdatafilename = "../SQLdata.txt"

class Translator:

	def __init__(self, translation_filename, SQLdata_filename):
		self.translation_filename = translation_filename
		self.SQLdata_filename = SQLdata_filename
		self.makeTranslator()
		self.formatQuery()
		self.translate()
		self.writeTDTF()

	def makeTranslator(self):
		translationfile = open(self.translation_filename, "r")
		mydict = {}

		for line in translationfile:
			temp = line.split("\t")

			if(temp[1] == "Char. Value\n"):
				mydict[temp[0]] = temp[0]

			else:
				mydict[temp[0]] = temp[1]

		self.mydict = mydict

	def formatQuery(self):
		SQLdatafile = open(self.SQLdata_filename, "r")
		
		SQLdata = []
		for line in SQLdatafile:
			SQLdata.append(line[line.find("[")+1:line.find("]")])

		self.SQLdata = SQLdata

	def translate(self):
		translatedData = []

		for columnName in self.SQLdata:
			if(columnName in self.mydict):
				translatedData.append(self.mydict[columnName][:-1])
			else:
				translatedData.append(columnName)

		self.translatedData = translatedData

	def writeTDTF(self, outfile="../outfile.txt"):
		ofile = open(outfile, "w")

		outdata = "SET ANSI_NULLS ON\nGO\n\nSET QUOTED_IDENTIFIER ON\nGO\n\nCREATE VIEW  AS\n"
		outdata += "SELECT\n"

		iter = 0
		for data in self.translatedData:
			outdata += "[" + self.SQLdata[iter] + "]" + " as " + "[" + data + "]," + "\n"
			iter += 1

		outdata += "FROM  AS COMP\nGO"
		ofile.write(outdata)


Translator(translationfilename, SQLdatafilename)
