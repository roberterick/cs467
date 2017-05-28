#list of our primary verbs
possibleVerbs = ['move', 'examine']

#possible variants of the word move
moveVariants = ['moving', 'moved', 'go', 'walk']
for b in moveVariants:
	possibleVerbs.append(b)

possibleDirections = ['north','south', 'east', 'west']
#possible variants of the different directions
northVariants = ['up']
eastVariants = ['right']
southVariants = ['down']
westVariants = ['left']

possiblePrepositions = []

def sagParser(userInput):
	inputList = userInput.split(' ')
	#sagParser hopefully returns a list that will list at 
	# [0] - action, then [1] - direction/object
	print inputList
	parserReturn = []
	foundVerb = verbFinder(inputList)
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
		print 'Your input has too many verbs'
	if verbCounter < 1: 
		print 'There are not enough verbs.'
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
		print 'Your input has too many directions'
	if directionCounter < 1: 
		print 'There are not enough directions.'
	if directionCounter == 1:
		return foundDirection