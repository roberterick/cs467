##class: CS467
##group: Sagitta - Dictionary
##members: Robert Erick, James Wong, Brent Nolan
##date: 5/29/2017

##things to do: 
##1. continually updated specialFeaturse and specialItems 

#list of our primary verbs
possibleVerbs = ['move', 'examine', 'get', 'drop', 'help', 'teleport']

# --MOVE--
#possible variants of the verb 'move'
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
#possible variants of the verb 'examine'
examineVariants = ['look', 'inspect', 'looked', 'looking', 'see', 'check', 'touch']
for b in examineVariants:
	possibleVerbs.append(b)

# --GET--
#possible variants of the verb 'get'
getVariants = ['take', 'hold', 'receive', 'took', 'pick']
for b in getVariants:
	possibleVerbs.append(b)

# --DROP--
#possible variants of the verb 'drop'
dropVariants = ['throw', 'dropped', 'dropping', 'remove']
for b in dropVariants:
	possibleVerbs.append(b)

# --HELP--
#possible variants of the verb 'help'
helpVariants = ['helpme']
for b in helpVariants:
	possibleVerbs.append(b)

# --TELEPORT--
#possible variants of the verb 'teleport'
teleportVariants = ['magic', 'teleporting']
for b in teleportVariants:
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