##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

import os
import json
import pickle
import ply
from our_objects import *
from sagParser import *

CURRENT_VERSION=1.2

class App(object):
    def __init__(self):
        print 'initializing'
        self.objects={}#dictionary holds rooms, the player, and items
        self.player=None
        self.initializeGame()
        playerkey=filter(lambda x:self.objects[x].type=='player',self.objects.keys())[0]
        self.player=self.objects[playerkey]
        self.mainLoop()#begin main loop

    def mainLoop(self):
        while(1):
            self.printCurrentLocation()
            res=self.processPrompt()
            if res=='exit':
                return
            elif res==False:
                print 'That command was not recognized!'
            
    def printCurrentLocation(self):
        location=self.player.location
        print self.objects[location]
##        print 'You are in: ',self.objects[location]
##        items=self.

    def processPrompt(self):
        '''
            returns 'exit' if the game is exit
            returns True if the command succeeded
            returns False if the command failed
        '''
        commands={
            'help':self.showHelp,
            'save game':self.saveGame,
            'load game':self.loadGame,
##            'print objects1':self.printObjects1,
##            'print objects2':self.printObjects2,
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
        elif splitcommand[0] in ['get','take']:
            if len(splitcommand)==2:
                cmd,theitem=splitcommand
                return self.player.getItem(theitem)
            else:
                return False
        elif splitcommand[0] in ['drop','throw']:
            if len(splitcommand)==2:
                cmd,theitem=splitcommand
                return self.player.dropItem(theitem)
            else:
                return False
        ## 'look command per the requirements of the project'
        elif splitcommand[0] in ['look'] and len(splitcommand)==1:
            print self.player.otherObjects[self.player.location].long_description
        elif splitcommand[0] in ['examine']:
            if len(splitcommand)>=2:
                cmd,item=splitcommand
                return self.player.examine(item)
            else:
                return False
        elif splitcommand[0] in ['teleport']:
            return self.player.teleport()
        elif splitcommand[0] in ['status']:
            print self.player
            return True
        elif splitcommand[0] in ['inventory']:
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
                return self.player.move(direction)
            if inputParseReturn[0] == 'examine':
                return self.player.examine(inputParseReturn[1])
            if inputParseReturn[0] == 'get':
                return self.player.getItem(inputParseReturn[1])
            if inputParseReturn[0] == 'drop':
                return self.player.dropItem(inputParseReturn[1])
            if inputParseReturn[0] == 'help':
                print "Are you asking for help? If so, here's what the 'help' command brings up:"
                self.showHelp()
            if inputParseReturn[0] == 'teleport':
                self.player.teleport()
                #objectItem = inputParseReturn[1]
                #return self.player.examine(direction)    

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
        '''
        print h
##        print objects1: print known objects
##        print objects2: print known objects

    def where(self):
        return os.getcwd()

    def initializeGame(self):
        answer=raw_input('Start a new game (y/n)?')
        answer=answer.lower()
        if answer=='y':
            self.initializeFromJSONFiles()
        else:
            self.loadGame()

    def initializeFromJSONFiles(self):
        pth=os.path.join(self.where(),'init')
        nonjsonpath=os.path.join(self.where(),'init','not_json')
        shortlist=os.listdir(pth)#file list without path
        longlist=[os.path.join(pth,x) for x in shortlist]#file list with path
        longlist=filter(lambda x:os.path.isfile(x),longlist)
        for f in longlist:
            text=open(f,'r').read()#read in the text
            try:
                data=json.loads(text)#convert to json
            except:
                print '*'*10,'File %s has incorrect json.  Please correct!'%f
                continue

            self.loadFormattedText(nonjsonpath,data)
            
            if data['type']=='room':
                newobj=Room(**data)
            elif data['type']=='player':
                newobj=Player(**data)
            elif data['type']=='feature':
                newobj=Feature(**data)
            elif data['type']=='item':
                newobj=Item(**data)
            elif data['type']=='version':
                newobj=Version(**data)
            else:
                assert False #shouldn't happen
            name=newobj.name.lower()#insure that all names should be lower
            if hasattr(newobj,'adjacent_rooms'):
                for k,v in newobj.adjacent_rooms.items():
                    if not k==k.lower():print 'problem with adjacent roomf for %s'%name
            self.objects[name]=newobj#add the object to our dictionary
            newobj.otherObjects=self.objects#gives all objects access to other objects

        self.linkFeatures()
        self.linkItems()
        self.objects['version'].version=CURRENT_VERSION
##        print self.objects

    def linkItems(self):
        for k,v in self.objects.items():#items here means k,v pairs
            if v.type!='item':continue
            location=v.location
            if not self.objects.has_key(location) and self.objects[location]['type']=='room':
                print 'Item %s does not have a valid location!'%k
            room=self.objects[location]
            if not k in room.items: room.items+=[k]

    def linkFeatures(self):
        for k,v in self.objects.items():#items here means k,v pairs
            if v.type!='feature':continue
            location=v.location
            if not self.objects.has_key(location) and self.objects[location]['type']=='feature':
                print 'Feature %s does not have a valid location!'%k
            room=self.objects[location]
            if not k in room.items: room.features+=[k]

    def loadFormattedText(self,textpath,datadict):
        #this loads in values from an alternate text files
        #so that formatting is improved
        #the file must exist
        #the name must be the value in the key
        for k,v in datadict.items():
            if str(type(v)) not in ["<type 'unicode'>","<type 'str'>"]:continue
            fullpath=os.path.join(textpath,v)
            if os.path.exists(fullpath):datadict[k]=open(fullpath,'r').read()       
        
    def loadGame(self):
        pth=os.path.join(self.where(),'saved')
        shortlist,longlist=self.returnSanitizedLists(pth)
        if len(shortlist)==0:
            print 'No saved games found!  Starting a new game.'
            self.initializeFromJSONFiles()
            return

        for i,f in enumerate(shortlist):#display saved games
            print '%02i.'%i,f
        a1=raw_input('Choose game to load (an integer):')
        a1=a1.lower()
        
        try:
            a1=int(a1)
        except:
            print 'Please enter an integer.'
            return

        target=None
        try:
            target=longlist[a1]
        except:
            print 'Please enter an integer from 0 to %i'%len(longlist)-1
            return
        self.loadObjectsDict(target)

    def loadObjectsDict(self,apath):
        fobj=open(apath, 'rb')
        self.objects=pickle.load(fobj)
        fobj.close()      

    def returnSanitizedLists(self,apath):
        shortlist=os.listdir(apath)#file list without path
        shortlist.sort()
        longlist=[os.path.join(apath,x) for x in shortlist]#file list with path
        for i in range(len(longlist)-1,-1,-1):
            target=longlist[i]

            with open(target, 'rb') as fobj:
                proposedObjects=None
                #see if a file is capable of loading
                try:
                    proposedObjects=pickle.load(fobj)
                except:
                    shortlist.pop(i)
                    longlist.pop(i)
                    continue
                #show only file containing the correct version
                if proposedObjects['version'].version!=CURRENT_VERSION:
                    shortlist.pop(i)
                    longlist.pop(i)
                    continue
        return shortlist,longlist

    def saveGame(self):
        answer=raw_input('Enter name to save:')
        answer=answer.lower()
        pth=os.path.join(self.where(),'saved','%s.pkl'%answer)
        #check if exists already
        if os.path.exists(pth):
            a2=raw_input('That file exists already. Overwrite (y/n)?')
            a2=a2.lower()
            if a2=='n':return
        fobj=open(pth, 'wb')
        pickle.dump(self.objects,fobj)
        fobj.close()

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
        
    def printObjects1(self):
        '''helper function to see what is there'''
        for k in self.objects:
            for k2 in dir(self.objects[k]):
                if not k2.startswith('_'):
                    print k2,':',eval('self.objects[k].%s'%k2)
            print
            
    def printObjects2(self):
        '''helper function to see what is there'''
        for k in self.objects:
            print self.objects[k]
            print

if __name__ == "__main__":
    app=App()
    print app.where()
