##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
import random
from objects.GameObj import GameObj
from objects.Item import Item

class Player(GameObj):
    def __init__(self,**data):
        super(Player,self).__init__()
        self.items=[]
        self.location=''
        self.seen=False
        self.status='you are trying to win.'
        self.__dict__.update(data)

    def __str__(self):
        items=sorted([self.otherObjects[itm].name for itm in self.items])
        inventory=', '.join(items)
        if inventory=='':inventory="nothing"
        status='Status: %s'%self.status
        if self.seen:
            desc=self.short_description
        else:
            desc=self.long_description
            self.seen=True

        thereturn='''
>>>>>>>>>>>>>>>>>STATUS<<<<<<<<<<<<<<
%s
Your location: %s
Your inventory: %s
Your status: %s
>>>>>>>>>>>>>END STATUS<<<<<<<<<<<<<<
        '''%(desc,self.location,inventory,self.status)
        return thereturn

    def printInventory(self):
        #fix for inventory print
        items=[]
        for a in self.items:
            items.append(a)
        #eliminate hidden items
        for item in items:
            obj=self.otherObjects[item]
            if obj.hidden==True:items.remove[item]
        #make the inventory
        inventory='\n'.join(items)
        if inventory=='':inventory="nothing"
        message='''
>>>>>>>>>>>>>>>>>INVENTORY<<<<<<<<<<<<<<
%s
>>>>>>>>>>>>>END INVENTORY<<<<<<<<<<<<<<
        '''%(inventory)
        print message
        return True

    def getItem(self,itemName):
        if not self.location in self.otherObjects:return False #location is bad
        room=self.otherObjects[self.location]
        if not itemName in room.items:return False #it isn't in the room
        if not self.otherObjects.has_key(itemName):return False #itemName not valid
        if not isinstance(self.otherObjects[itemName],Item):return False #not an item
        item=self.otherObjects[itemName]
        if hasattr(item,'hidden') and item.hidden:return False #hidden items not takeable
        self.items+=[itemName]#add to our items
        room.items.remove(itemName)#remove from the room
        print 'You have added the %s to your inventory.'%itemName
        self.checkWin()
        return True
    
    def dropItem(self,itemName):
        if not itemName in self.items:return False #we don't have the item
        if not self.location in self.otherObjects:return False #room is bad
        room=self.otherObjects[self.location]
        room.items+=[itemName]
        self.items.remove(itemName)
        print 'You have dropped the %s.'%itemName
        return True

    def checkWin(self):
        '''checks to see if the game has been won'''
        if'core restoration medal' in self.items \
        and 'control transfer medal' in self.items:
            self.status='you have won the game!'
            print 'You have repaired the engine core and transferred control to the auxiliary \nbridge.  You have won the game!'
            exit(0)
        
    def move(self,direction):
        #test for the room
##       if not self.location in self.otherObjects:
##            return False
        #get the room
        ##remove clearScreens() if you don't like how it clears screen after moving to a new space
        room=self.otherObjects[self.location]
        #test for existence of direction in room.adjacent_rooms
        if not room.adjacent_rooms.has_key(direction):#is room in adjacent rooms?
            print 'Problem: one way movement in room %s moving %s!'%(room.name,direction)
            return False

        if direction in room.locked_directions:
            print 'That way appears to be locked!'
            return False
        elif direction in room.adjacent_rooms:
            self.location = room.adjacent_rooms[direction]
            self.clearScreen()
##            self.checkWin()
            return True
        elif direction in room.adjacent_rooms.itervalues():
            self.location = direction
            self.clearScreen()
##            self.checkWin()
            return True
        #if bad, exit false
        else:
            self.clearScreen()
##            self.checkWin()
            return False
        
    def examine(self,itemName):
        if not self.location in self.otherObjects:
            return False

        adict=self.getNameAndAlternates()
        if not itemName in adict.keys():
            print "This room does not have that item or feature!"
            return False

        realName=adict[itemName]
        item=self.otherObjects[realName]

        if hasattr(item,'canUnlock') and item.canUnlock==True:
            item.unlockAllDirections()
        if hasattr(item,'canUnhide') and item.canUnhide==True:
            item.unhideAll()
            
        
        t=item.type
        t.capitalize()
        print item.long_description
        return True

    def getNameAndAlternates(self):
        adict={}
        room=self.otherObjects[self.location]
        #jimmy - added player items to adict
        for name in room.items+room.features+self.items:
            obj=self.otherObjects[name]
            alternateNames=obj.alternate_names
            for an in alternateNames:
                adict[an]=name#make alternate->object
        for name in room.items+room.features+self.items:
            adict[name]=name#make object->object, for completeness
        return adict

    def teleport(self):
        rooms=[]
        for s in self.otherObjects:
            if self.otherObjects[s].type=='room':rooms+=[s]
        theroom=random.choice(rooms)
        self.clearScreen()
        phrases=["It feels as if you are swimming in a deep pool of warm water."]
        phrases+=["There are swirling lights and you are disoriented.  The bile is rising in your throat."]
        phrases+=["Your body feels as if it is being torn apart."]
        thephrase='You are teleporting to room %s!  %s\n'%(theroom,random.choice(phrases))
        self.location=theroom
        print thephrase
        return True

    def use(self, itemName, featureName, verb):
        room = self.otherObjects[self.location]
        feature = self.otherObjects[featureName]
        if not itemName in self.items:
            print 'You do not have that item'
            return False  # we don't have the item
        if not room.name in feature.location:
            print 'Feature is not in this room'
            return False #feature not in this room
        if not verb in feature.verb_use:
            print 'You cannot %s %s!'%(verb,featureName)
            return False
        if not itemName in feature.item_use:
            print 'You cannot use %s on %s!' %(itemName, featureName)
            return False
        else:
            print '%s' %feature.result_text
            feature.long_description = feature.description_change
            if feature.result_item:
                rItem = self.otherObjects[feature.result_item]
                rItem.hidden = False
                self.getItem(rItem.name)
            item=self.otherObjects[itemName]
            item.unlockAllDirections()
            if feature.destroy_item:
                item.hidden = True
                room.items += [itemName]
                self.items.remove(itemName)
            return True

    def secretjump(self,roomName):
        if roomName not in self.otherObjects:return False
        if self.otherObjects[roomName].type!='room':return False
        self.clearScreen()
        self.location=roomName
        return True

if __name__=='__main__':
    p=Player()
    print dir(p)
