##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

import os
import platform
from objects import *
from sagParser import *


class App(AppBase):
    def __init__(self):
        super(App,self).__init__()
        self.initializeGame()
        playerkey=filter(lambda x:self.objects[x].type=='player',self.objects.keys())[0]
        self.player=self.objects[playerkey]
        self.mainLoop()#begin main loop

    def mainLoop(self):
        enteringRoomTracker = [True]
        while(1):
            if enteringRoomTracker == [True]:
                self.printCurrentLocation()
            res=self.processPrompt(enteringRoomTracker)
            if res=='exit':
                return
            elif res==False:
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                print 'That command was not recognized!'
            
    def printCurrentLocation(self):
        location=self.player.location
        print self.objects[location]
##        print 'You are in: ',self.objects[location]
##        items=self.

    def processPrompt(self,enteringRoomTracker):
        '''
            returns 'exit' if the game is exit
            returns True if the command succeeded
            returns False if the command failed
        '''
        commands={
            'help':self.showHelp,
            'save game':self.saveGame,
            'load game':self.loadGame,
          }

        print
        print "(type 'help' for commands)",
        userInput=raw_input(">>>>")#prompt
        userInput=userInput.lower()
        splitcommand=userInput.split(' ',1)
        
        if userInput=='exit':
            #implement exit, temp save if dirty?
            return 'exit'
        elif commands.has_key(userInput):
            commands[userInput]()
            return True
##        elif splitcommand[0] in ['get','take']:
##            if len(splitcommand)==2:
##                cmd,theitem=splitcommand
##                enteringRoomTracker.pop(0)
##                enteringRoomTracker.append(False)
##                return self.player.getItem(theitem)
##            else:
##                enteringRoomTracker.pop(0)
##                enteringRoomTracker.append(False)
##                return False
##       elif splitcommand[0] in ['drop','throw']:
##            if len(splitcommand)==2:
##                cmd,theitem=splitcommand
##                enteringRoomTracker.pop(0)
##                enteringRoomTracker.append(False)
##                return self.player.dropItem(theitem)
##            else:
##                return False
        ## 'look command per the requirements of the project'
        elif splitcommand[0] in ['look'] and len(splitcommand)==1:
            enteringRoomTracker.pop(0)
            enteringRoomTracker.append(False)
            print self.player.otherObjects[self.player.location].long_description
##        elif splitcommand[0] in ['examine']:
##            if len(splitcommand)>=2:
##                cmd,item=splitcommand
##                enteringRoomTracker.pop(0)
##                enteringRoomTracker.append(False)
##                return self.player.examine(item)
##            else:
##                return False
        elif splitcommand[0] in ['teleport']:
            enteringRoomTracker.pop(0)
            enteringRoomTracker.append(True)
            return self.player.teleport()
        elif splitcommand[0] in ['secretjump']:
            enteringRoomTracker.pop(0)
            enteringRoomTracker.append(True)
            return self.player.secretjump(splitcommand[1])
        elif splitcommand[0] in ['status']:
            enteringRoomTracker.pop(0)
            enteringRoomTracker.append(False)
            print self.player
            return True
        elif splitcommand[0] in ['inventory'] and len(splitcommand)==1:
            enteringRoomTracker.pop(0)
            enteringRoomTracker.append(False)
            return self.player.printInventory()
        else:
            # --PARSER --
            currentRoom = self.player.otherObjects[self.player.location]
            currentItems = self.player.items

            inputParseReturn = specialSagParser(userInput,currentRoom)
            if inputParseReturn == None:
                inputParseReturn = sagParser(userInput,currentRoom, currentItems)
            
            if inputParseReturn == None:
                return False

            if inputParseReturn[0] == 'move':
                direction = inputParseReturn[1]
                #FIX FOR ELEVATOR DIRECTIONS "UP" AND "DOWN"
                if self.player.location == 'elevator level 1': 
                    if direction == 'south':
                        direction = 'down'
                if self.player.location == 'elevator level 2':
                    if direction == 'south':
                        direction = 'down'
                    if direction == 'north':
                        direction = 'up'
                if self.player.location == 'elevator level 3':
                    if direction == 'north':
                        direction = 'up'
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(True)
                return self.player.move(direction)
            if inputParseReturn[0] == 'examine':
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                return self.player.examine(inputParseReturn[1])
            if inputParseReturn[0] == 'get':
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                return self.player.getItem(inputParseReturn[1])
            if inputParseReturn[0] == 'drop':
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                return self.player.dropItem(inputParseReturn[1])
            if inputParseReturn[0] == 'help':
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                print "Are you asking for help? If so, here's what the 'help' command brings up:"
                self.showHelp()
                return True
            if inputParseReturn[0] == 'teleport':
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(True)
                self.player.teleport()
                return True
            if inputParseReturn[0] == 'use':
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                if '' in inputParseReturn:
                    print "You must use one item with one feature"
                    return False
                else:return self.player.use(inputParseReturn[1],inputParseReturn[2], inputParseReturn[3])

                #objectItem = inputParseReturn[1]
                #return self.player.examine(direction)
            else:
                enteringRoomTracker.pop(0)
                enteringRoomTracker.append(False)
                return False
    def showHelp(self):
        h='''
save game: save the current game
load game: load a saved game    
exit: exit the game

look: repeats the long form explanation of the room
examine <feature>: examines a feature
examine <item>: examines an item
inventory: shows your items
move <direction>: moves the player in a direction
status: shows your status
teleport: teleports to (possibly another) room
use <item> <feature>: Use an item on a feature
feed <item> <feature>:  Feed an item to a feature
        '''
        print h

    def normalizeDirection(self,direction):
        aMap={
            'forward':'north',
            'aft':'south',
            'starboard':'east',
            'port':'west',
              }
        if aMap.has_key(direction):
            return aMap[direction]
        else:
            return direction
        

if __name__ == "__main__":
    app=App()
    print app.where()
