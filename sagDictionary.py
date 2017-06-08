##class: CS467
##group: Sagitta - Dictionary
##members: Robert Erick, James Wong, Brent Nolan
##date: 5/29/2017

##things to do: 
##1. continually updated specialFeaturse and specialItems 

#list of our primary verbs
possibleVerbs = ['move', 'examine', 'get', 'drop', 'help', 'teleport', 'use']

#list of specialphrases
# [save game, load game, exit, look (long form), inventory, status]
#list of variants of special verbs
specialVerbs = []

# --MOVE--
#possible variants of the verb 'move'
moveVariants = ['moving', 'moved', 'go', 'walk', 'going', 'walk', 'walking', 'walked']
for b in moveVariants:
	possibleVerbs.append(b)
#insert multi word phrases of MOVE
specialMoveVariants = []
for b in specialMoveVariants:
	specialVerbs.append(b)

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
#insert multi word phrases of EXAMINE
specialExamineVariants = ['check out', 'what is']
for b in specialExamineVariants:
	specialVerbs.append(b)

# --GET--
#possible variants of the verb 'get'
getVariants = ['take', 'hold', 'receive', 'took', 'pick']
for b in getVariants:
	possibleVerbs.append(b)
#insert multi word phrases of GET
specialGetVariants = []
for b in specialGetVariants:
	specialVerbs.append(b)

# --DROP--
#possible variants of the verb 'drop'
dropVariants = ['throw', 'dropped', 'dropping', 'remove']
for b in dropVariants:
	possibleVerbs.append(b)
#insert multi word phrases of DROP
specialDropVariants = []
for b in specialDropVariants:
	specialVerbs.append(b)

# --HELP--
#possible variants of the verb 'help'
helpVariants = ['helpme']
for b in helpVariants:
	possibleVerbs.append(b)
#insert multi word phrases of HELP
specialHelpvariants = []
for b in specialHelpvariants:
	specialVerbs.append(b)

# --TELEPORT--
#possible variants of the verb 'teleport'
teleportVariants = ['magic', 'teleporting']
for b in teleportVariants:
	possibleVerbs.append(b)
#insert multi word phrases of TELEPORT
specialTeleportVariants = []
for b in specialTeleportVariants:
	specialVerbs.append(b)

# --USE--
#possible variants of the verb 'use'
useVariants = ['feed', 'open', 'repair', 'screw', 'unscrew', 'unlock', 'fill', 'refill', 'type', 'replace']
for b in useVariants:
	possibleVerbs.append(b)
#insert multi word phrases of USE
specialUseVariants = []
for b in specialUseVariants:
	specialVerbs.append(b)

# list of features that are longer than one word
specialFeatures = ['table of notes', 'alien notes', 'dying alien', 'dying man', 'pistol instructions', 'entertainment terminal', 'vacsuit locker', 'oxygen tank', 'airlock control', 'transfer controls', 'cargo containers', 'manifest terminal', 'auxiliary helm', 'capacitor housing']

# list of items that are longer than one word
specialItems = ['core restoration medal', 'blue rose', 'hibernation pod', 'plastic pass key', 'blaster pistol', 'reactor fuel', 'model ship', 'gold medallion', 'control transfer medal', 'security chip', 'auxiliary codes', 'depleted vacsuit', 'restored vacsuit', 'core capacitor']

# --PREPOSITIONS--
possiblePrepositions = []

# --SPECIAL CHARACTERS--
#possible special characters that should be removed from words in 
#userinput
possibleSpecialChars = " ?.!/;:,"