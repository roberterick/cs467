##class: CS467
##group: Sagitta - Dictionary
##members: Robert Erick, James Wong, Brent Nolan
##date: 5/29/2017

##things to do: 
##1. continually updated specialFeaturse and specialItems 

#list of our primary verbs
possibleVerbs = ['move', 'examine', 'get']

# --MOVE--
#possible variants of the word 'move'
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

# --EXAMINE--
#possible variants of the word 'examine'
examineVariants = ['look', 'inspect', 'looked', 'looking' ]
for b in examineVariants:
	possibleVerbs.append(b)

# --GET--
#possible variants of the word 'get'
getVariants = ['take', 'touch', 'hold', 'receive', 'took']
for b in getVariants:
	possibleVerbs.append(b)

# list of features that are longer than one word
specialFeatures = ['table of notes', 'alien notes', 'dying alien', 'dying man', 'pistol instructions']

# list of items that are longer than one word
specialItems = ['bronze medallion', 'bridge button', 'blue rose', 'hibernation pod', 'plastic pass key', 'blaster pistol', 'reactor fuel', 'model ship', 'gold medallion', 'silver medallion']

# --PREPOSITIONS--
possiblePrepositions = []

# --SPECIAL CHARACTERS--
#possible special characters that should be removed from words in 
#userinput
possibleSpecialChars = " ?.!/;:,"