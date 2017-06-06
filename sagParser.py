##class: CS467
##group: Sagitta - Parser
##members: Robert Erick, James Wong, Brent Nolan
##date: 5/29/2017

##things to do: 
##1. update parser so it works with other verbs: [ADD?]
##2. make 'move' work with room names - done 05/29/2017

##when adding new verb, things to update:
## (here) def sagParser
## (here) def verbFinder
## (in sagDictionary.py) - possibleVerbs, [verb]Variants
## (in sagitta.py) - def processPrompt

from sagDictionary import *



#special parser that checks whether user input is single string of either
## [1] direction (north, east, etc) or [2] adjacent room nap
def specialSagParser(userInput, roomObject):
        parserReturn = []
        adjacentRooms = roomObject.adjacent_rooms
        adjRoomAsVerb = []
        directionAsVerb = []
        if 'north' in adjacentRooms:
            directionAsVerb.append('north')
            adjRoomAsVerb.append(adjacentRooms['north'])
        if 'east' in adjacentRooms:
            directionAsVerb.append('east')
            adjRoomAsVerb.append(adjacentRooms['east'])
        if 'south' in adjacentRooms:
            directionAsVerb.append('south')
            adjRoomAsVerb.append(adjacentRooms['south'])
        if 'west' in adjacentRooms:
            directionAsVerb.append('west')
            adjRoomAsVerb.append(adjacentRooms['west'])
        if 'up' in adjacentRooms:
            directionAsVerb.append('up')
            adjRoomAsVerb.append(adjacentRooms['up'])
        if 'down' in adjacentRooms:
            directionAsVerb.append('down')
            adjRoomAsVerb.append(adjacentRooms['down'])

        index = -1;
        for a in adjRoomAsVerb:
            index += 1;
            if userInput == a:
                parserReturn.append('move')
                parserReturn.append(directionAsVerb[index])
                return parserReturn

        index = -1;
        for a in directionAsVerb:
            index += 1
            if userInput == a:
                parserReturn.append('move')
                parserReturn.append(directionAsVerb[index])
                return parserReturn

#sagParser hopefully returns a list that will list at 
# [0] - action, then [1] - direction/item
def sagParser(userInput, roomObject, playerItems):
    #separating the user input by space
    inputList = userInput.split(' ')
    global actualVerb
    actualVerb = ''
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
    
    #special hard coded verb synonyms
    if foundVerb == None:
        possibleSpecialWordsCounter = 0
        for a in specialVerbs:
            if userInput.find(a) != -1:
                possibleSpecialWordsCounter += 1
                foundVerb = a
        if possibleSpecialWordsCounter == 1:
            if foundVerb in specialMoveVariants: foundVerb = 'move'
            if foundVerb in specialExamineVariants: foundVerb = 'examine'
            if foundVerb in specialGetVariants: foundVerb = 'get'
            if foundVerb in specialDropVariants: foundVerb = 'drop'
            if foundVerb in specialHelpvariants: foundVerb = 'help'
            if foundVerb in specialTeleportVariants: foundVerb = 'teleport'

    #conditionals that execute depending on the string in the foundVerb
    if foundVerb == 'move':
        ##creating a list of the possible rooms that the user can go into
        possibleRooms = []
        adjacentRooms = roomObject.adjacent_rooms
        if 'north' in adjacentRooms:
            possibleRooms.append(adjacentRooms['north'])
        if 'east' in adjacentRooms:
            possibleRooms.append(adjacentRooms['east'])
        if 'south' in adjacentRooms:
            possibleRooms.append(adjacentRooms['south'])
        if 'west' in adjacentRooms:
            possibleRooms.append(adjacentRooms['west'])
        if 'up' in adjacentRooms:
            possibleRooms.append(adjacentRooms['up'])
        if 'down' in adjacentRooms:
            possibleRooms.append(adjacentRooms['down'])

        ##checking if the userInput has any of the possible rooms in the input
        possibleRoomsCounter = 0
        foundRoom = ''
        for a in possibleRooms:
            if userInput.find(a) != -1:
                possibleRoomsCounter += 1
                foundRoom = a

        if possibleRoomsCounter == 1:
            ##finding key by value room name()
            ##source: https://stackoverflow.com/questions/23295315/get-key-by-value-dict-python
            for k, v in adjacentRooms.items():
                if foundRoom in v:
                    parserReturn.append(foundVerb)
                    if k == 'up':
                        parserReturn.append('north')
                    elif k == 'down':
                        parserReturn.append('south')
                    else:
                        parserReturn.append(k)
                    return parserReturn

        elif possibleRoomsCounter > 1:
            print "You tried going to two places at once!"

        else:
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
        ##appending items from playerItems (inventory)
        for c in playerItems:
            roomFeaturesAndItems.append(c)

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

        ##appending the specicalWordsList with  special items
        for c in specialItems:
            specialWordsList.append(c)

        #checking whether the user input has a special words
        #if so, appending to the userinputList
        specialWordFinder(userInput,specialWordsList,inputList)

        #checking whether there is item in the inputlist
        foundItems = itemsAndFeaturesFinder(inputList,roomItems)
        parserReturn.append(foundVerb)
        parserReturn.append(foundItems)
        return parserReturn

    if foundVerb == 'drop':
        specialWordsList = []
        ##appending the specicalWordsList with special items
        for c in specialItems:
            specialWordsList.append(c)

        #checking whether the user input has a special word
        #if so, appending to the userinputList
        specialWordFinder(userInput,specialWordsList,inputList)

        #checking whether there is item in the inputlist (command broken down)
        # and if the player has that item
        playerItemCounter = False
        playerItemToPass =[]
        for i in inputList:
            for j in playerItems:
                if i == j:
                    playerItemCounter = True
                    playerItemToPass = i

        #if player has that item and he wants to drop it, passing up
        if playerItemCounter == True:
            parserReturn.append(foundVerb)
            parserReturn.append(playerItemToPass)
            return parserReturn

        #else kicking out an error
        if playerItemCounter == False:
            print 'Are you sure you have that item?'

    if foundVerb == 'help':
        parserReturn.append(foundVerb)
        return parserReturn

    if foundVerb == 'teleport':
        parserReturn.append(foundVerb)
        return parserReturn

    if foundVerb == 'use':
        roomFeatures = []
        specialWordsListItem = []
        specialWordsListFeatures = []

        ##appending the specicalWordsList with special items
        for c in specialItems:
            specialWordsListItem.append(c)

        # checking whether the user input has a special word
        # if so, appending to the userinputList
        specialWordFinder(userInput, specialWordsListItem, inputList)

        # checking whether there is item in the inputlist (command broken down)
        # and if the player has that item
        playerItemCounter = False
        playerItemToPass = []
        for i in inputList:
            for j in playerItems:
                if i == j:
                    playerItemCounter = True
                    playerItemToPass = i

        # if player has that item start building the use array
        if playerItemCounter == True:
            parserReturn.append(foundVerb)
            parserReturn.append(playerItemToPass)

        # else kicking out an error
        if playerItemCounter == False:
            print 'Are you sure you have that item?'


        #getting list of features in the room and appending to roomFeaturesAndItems List

        for b in roomObject.features:
            roomFeatures.append(b)

        ##appending the specicalWordsList with both special features

        for d in specialFeatures:
            specialWordsListFeatures.append(d)

        #checking whether the user input has and special words
        #if so, appending to the userinputList
        specialWordFinder(userInput,specialWordsListFeatures,inputList)

        #checking whether there is feature in inputlist
        foundF = featuresFinder(inputList,roomFeatures)
        parserReturn.append(foundF)
        if actualVerb == '': actualVerb = foundVerb
        parserReturn.append(actualVerb)
        return parserReturn
#checks if there's a possible verb in the command from the possibleVerbs array
#returns it if found			
def verbFinder(inputList):
    global actualVerb
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
        #checking if the found verb is a variant of one of our primary verbs
        for z in moveVariants:
            if foundVerb == z:
                foundVerb = 'move'
        for z in examineVariants:
            if foundVerb == z:
                foundVerb = 'examine'
        for z in getVariants:
            if foundVerb == z:
                foundVerb = 'get'
        for z in dropVariants:
            if foundVerb == z:
                foundVerb = 'drop'
        for z in helpVariants:
            if foundVerb == z:
                foundVerb = 'help'
        for z in teleportVariants:
            if foundVerb == z:
                foundVerb = 'teleport'
        for z in useVariants:
            if foundVerb == z:
                actualVerb = foundVerb
                foundVerb = 'use'
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

# checks if there's a possible direction in the command from the possibleDirections array	
# returns it if found					
def featuresFinder(inputList, fList):
    fCounter = 0
    foundF = ''
    for n in inputList:
        for k in fList:
            if n == k:
                fCounter += 1
                foundF = n
    if fCounter > 1:
        print 'Your input has too many features.'
        return foundF
    if fCounter < 1:
        print 'Your input does not have a feature.'
        return foundF
    if fCounter == 1:
        return foundF
##checks whether a word from specialWordsList is present in the inputList
##if so, appends the specialWord to an argument (listToAppend) List
## source: https://www.tutorialspoint.com/python/string_find.htm
def specialWordFinder (inputList, specialWordsList, listToAppend):
    for a in specialWordsList:
        if inputList.find(a) != -1:
                listToAppend.append(a)