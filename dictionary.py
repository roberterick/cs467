##class: CS467
##group: Sagitta - Parser/Dictionary
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

#list of our primary verbs
possibleVerbs = ['move', 'examine']

# --MOVE--
#possible variants of the word move
moveVariants = ['moving', 'moved', 'go', 'walk', 'going', 'walk', 'walking', 'walked']
for b in moveVariants:
	possibleVerbs.append(b)

# --MOVE--
#possible variants of the word move
examineVariants = ['look', 'inspect', 'looked', 'looking' ]
for b in examineVariants:
	possibleVerbs.append(b)

# --DIRECTIONS--
possibleDirections = ['north','south', 'east', 'west']

#possible variants of the different directions
northVariants = ['up', 'N']
eastVariants = ['right', 'E']
southVariants = ['down', 'S']
westVariants = ['left', 'W']

#appending direction variants to possible directions
for b in northVariants:
	possibleDirections.append(b)
for b in eastVariants:
	possibleDirections.append(b)
for b in southVariants:
	possibleDirections.append(b)
for b in westVariants:
	possibleDirections.append(b)

# list of features that are longer than one word
specialFeatures = ['table of notes', 'alien notes', 'dying alien', 'dying man', 'pistol instructions']

# list of objects that are longer than one word
specialItems = ['bronze medallion', 'bridge button', 'blue rose', 'hibernation pod', 'plastic pass key', 'blaster pistol', 'reactor fuel', 'model ship', 'gold medallion', 'silver medallion']

# --PREPOSITIONS--
possiblePrepositions = []

# --SPECIAL CHARACTERS--
#possible special characters that should be removed from words in 
#userinput
possibleSpecialChars = " ?.!/;:,"

#sagParser hopefully returns a list that will list at 
# [0] - action, then [1] - direction/object
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