##class: CS467
##group: Sagitta - Parser
##members: Robert Erick, James Wong, Brent Nolan
##date: 5/29/2017

##things to do: 
##1. update parser so it works with other verbs: 1) drop
##2. make 'move' work with room names

##when adding new verb, things to update:
## (here) def sagParser
## (here) def verbFinder
## (in sagDictionary.py) - possibleVerbs, [verb]Variants
## (in sagitta.py) - def processPrompt

from sagDictionary import *

#sagParser hopefully returns a list that will list at 
# [0] - action, then [1] - direction/item
def sagParser(userInput, roomObject):
	#separating the user input by space
	inputList = userInput.split(' ')
	
	#remove special characters from strings in inputList
	#based off of: 
	#https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
	for line in inputList:
		for char in line:
		    if char in possibleSpecialChars:
		        line1 = line.replace(char,'')
		        inputList.remove(line)
		        inputList.append(line1)

	#list of returned strings
	parserReturn = []

	#looking for verb in the inputList
	foundVerb = verbFinder(inputList)

	#if the found verb is move
	if foundVerb == 'move':
		foundDirection = directionFinder(inputList)
		if foundDirection != '':
			parserReturn.append(foundVerb)
			parserReturn.append(foundDirection)
			return parserReturn

	if foundVerb == 'examine':
		roomFeaturesAndItems = []
		specialWordsList = []

		#getting list of items AND features in the room and appending to roomFeaturesAndItems List
		for a in roomObject.items:
			roomFeaturesAndItems.append(a)
		for b in roomObject.features:
			roomFeaturesAndItems.append(b)

		##appending the specicalWordsList with both special items AND features
		for c in specialItems:
			specialWordsList.append(c)
		for d in specialFeatures:
			specialWordsList.append(d)

		#checking whether the user input has and special words
		#if so, appending to the userinputList
		specialWordFinder(userInput,specialWordsList,inputList)

		#checking whether there is feature or item in the inputlist
		foundIandF = itemsAndFeaturesFinder(inputList,roomFeaturesAndItems)
		parserReturn.append(foundVerb)
		parserReturn.append(foundIandF)
		return parserReturn

	if foundVerb == 'get':
		roomItems = []
		specialWordsList = []

		#getting list of items in the room and appending to roomFeaturesAndItems List
		for a in roomObject.items:
			roomItems.append(a)

		##appending the specicalWordsList with both special items
		for c in specialItems:
			specialWordsList.append(c)

		#checking whether the user input has and special words
		#if so, appending to the userinputList
		specialWordFinder(userInput,specialWordsList,inputList)

		#checking whether there is feature or item in the inputlist
		foundItems = itemsAndFeaturesFinder(inputList,roomItems)
		parserReturn.append(foundVerb)
		parserReturn.append(foundItems)
		return parserReturn

#checks if there's a possible verb in the command from the possibleVerbs array
#returns it if found			
def verbFinder(inputList):
	verbCounter = 0
	foundVerb = ''
	for n in inputList:
		for k in possibleVerbs:
				if n == k:
					verbCounter += 1
					foundVerb = n
	if verbCounter > 1:
		print 'Your input has too many verbs.'
	if verbCounter < 1: 
		print 'Your input does not have a verb (think move, go, etc.).'
	if verbCounter == 1:
		#checking if the found verb is a variant of the word 'move'
		for z in moveVariants:
			if foundVerb == z:
				foundVerb = 'move'
		for z in examineVariants:
			if foundVerb == z:
				foundVerb = 'examine'
		for z in getVariants:
			if foundVerb == z:
				foundVerb = 'get'
		return foundVerb

#checks if there's a possible direction in the command from the possibleDirections array
#returns it if found						
def directionFinder(inputList):
	directionCounter = 0
	foundDirection = ''
	for n in inputList:
		for k in possibleDirections:
				if n == k:
					directionCounter += 1
					foundDirection = n
	if directionCounter > 1:
		print 'Your input has too many directions.'
	if directionCounter < 1: 
		print 'Your input does not have a direction (think up, down, north, south).'
	if directionCounter == 1:
		for z in northVariants:
			if 	foundDirection == z:
				foundDirection = 'north'
		for z in eastVariants:
			if 	foundDirection == z:
				foundDirection = 'east'
		for z in southVariants:
			if 	foundDirection == z:
				foundDirection = 'south'
		for z in westVariants:
			if 	foundDirection == z:
				foundDirection = 'west'
		return foundDirection

#checks if there's a possible direction in the command from the possibleDirections array	
#returns it if found					
def itemsAndFeaturesFinder(inputList,oAndFList):
	iAndFCounter = 0
	foundIandF = ''
	for n in inputList:
		for k in oAndFList:
				if n == k:
					iAndFCounter += 1
					foundIandF = n
	if iAndFCounter > 1:
		print 'Your input has too many items/features.'
	if iAndFCounter < 1: 
		print 'Your input does not have an items or feature (look around you!).'
	if iAndFCounter == 1:
		return foundIandF

##checks whether a word from specialWordsList is present in the inputList
##if so, appends the specialWord to an argument (listToAppend) List
## source: https://www.tutorialspoint.com/python/string_find.htm
def specialWordFinder (inputList, specialWordsList, listToAppend):
	for a in specialWordsList:
		if inputList.find(a) != -1:
				listToAppend.append(a)