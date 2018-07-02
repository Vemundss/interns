import xml.etree.ElementTree as ET

translationfilename = "../translation.txt"
SQLdatafilename = "../SQLdata.txt"
formattedSQLdata = "../formattedSQLdata.txt"

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

		iter = 0
		for line in translationfile:
			temp = line.split("\t")

			if(temp[0] in mydict):
				#if temp[1].lower()!=mydict[temp[0]].lower():
				if temp[1]!=mydict[temp[0]]:
					if(temp[1] != ("Char. Value\n")):

						print(iter, temp[0], temp[1][:-1], mydict[temp[0]])
						iter+= 1

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

		i = 0
		for columnName in self.SQLdata:
			if(columnName in self.mydict):
				translatedData.append(self.mydict[columnName])
			else:
				translatedData.append("Need Mapping {}".format(i))
				i += 1

		self.translatedData = translatedData

	def writeTDTF(self, outfile="../outfile.txt"):
		ofile = open(outfile, "w")

		outdata = "SET ANSI_NULLS ON\nGO\n\nSET QUOTED_IDENTIFIER ON\nGO\n\nCREATE VIEW  AS\n"
		outdata += "SELECT\n"

		iter = 0
		for data in self.translatedData:
			if(data[-1] == "\n"):
				outdata += "[" + self.SQLdata[iter] + "]" + " as " + "[" + data[:-1] + "]," + "\n"
			else:
				outdata += "[" + self.SQLdata[iter] + "]" + " as " + "[" + data + "]," + "\n"
			iter += 1

		outdata += "FROM  AS COMP\nGO"
		ofile.write(outdata)


class xmlTranslator:

	def __init__(self, xml_filename):
		self.xml_filename = xml_filename

	def printXmlFIle(self):
		tree = ET.parse(self.xml_filename)
		root = tree.getroot()

		formattedSQLData = open("../formattedSQLdata.txt", "w")
		for minorRoot in root[0][0].findall("{http://schemas.microsoft.com/ado/2008/09/edm}EntityType"):
			#tmpstr = minorRoot.get("Name")
			#formattedSQLData.write("\n" + tmpstr + "\n\n")
			for child in minorRoot.findall("{http://schemas.microsoft.com/ado/2008/09/edm}Property"):
				tempString = child.get("Name") + "\t" + child.get("{http://www.sap.com/Protocols/SAPData}label") + "\n"
				#tempString = "{}".format(tempString)
				#tempString = tempString.split()[0] + "\t" + tempString.split()[1]
				formattedSQLData.write(tempString)
				#print(tempString.find("\t"))
				#print(child.get("Name"), child.get("{http://www.sap.com/Protocols/SAPData}label"))
		



objectBigBOI = xmlTranslator("../data.xml")
objectBigBOI.printXmlFIle()

Translator(formattedSQLdata, SQLdatafilename)


"""
Just take a decision on all of the similarities in the translation file. Remember to document
the mapping (i.e the decisions that has been made).

Aedat = Changed on
Erdat = Created on
Ernam = Created by
Brgew = Weight or Gross Weight (depending on table)
Gewei = Unit of weight
Loekz = Deletion flag
Werks = Plant

This work might be easiest implemented in a manual manner in the translation file
Afterwards the script can be run using different SQLdata.txt files but keeping the translation file (make sure not to run generation of translation file
after manual insertion of translation file (so it wont be overwritten)
Copy paste output from outfile.txt into SQL, then done :)

OBS: cannot find gewei/brgew, might not last two either. Check if script actually creates all translations
"""