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

# --PREPOSITIONS--
possiblePrepositions = []

# --SPECIAL CHARACTERS--
#possible special characters that should be removed from words in 
#userinput
possibleSpecialChars = " ?.!/;:,"

#sagParser hopefully returns a list that will list at 
# [0] - action, then [1] - direction/object
def sagParser(userInput):
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

#checks if there's a possible verb in the command from the possibleVerbs array			
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
		return foundVerb

#checks if there's a possible direction in the command from the possibleDirections array			
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