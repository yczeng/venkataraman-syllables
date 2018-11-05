''' helper functions available to import '''

import ast
import re

def getArrayFromTextFile(filepath, lineIndex):
	'''
	returns an array from a text file's string of an array
	this only works if textfile is on one line
	'''

	with open(filepath, "r") as text:
		for index, line in enumerate(text):
			if index == lineIndex:
				return ast.literal_eval(line)

	raise Exception('Index is out of bounds, or filepath not correct.')

# utterances = getArrayFromTextFile('../splitByUtterance.txt', 0)

# with open('../textUtterance.txt','a') as newData:
# 	for eachUtterance in utterances:
# 		newData.write(str(eachUtterance) + "\n")


with open('../data/mother.speech.txt', "r") as text:
	for index, line in enumerate(text):
		line = re.sub("\d+", "", line)
		line = line.replace("U", "\n")
		line = line.replace("W", " ")
		line = line.replace("P", "")

		with open('../data/new.mother.speech.txt','a') as newData:
			newData.write(str(line))
