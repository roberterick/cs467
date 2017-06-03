##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
import random

class GameObj(object):
    def __init__(self):
        self.otherObjects=None
        self.long_description=''
        self.short_description=''
        self.name=''
        self.alternate_names=[]
        self.type=''

class Version(GameObj):
    def __init__(self,**data):
        self.version=0.0
        self.__dict__.update(data)       
        
class Item(GameObj):
    def __init__(self,**data):
        self.location=''
        self.seen=False
        self.hidden=False
        self.alternate_names=[]
        self.__dict__.update(data)
    def __str__(self):
        if self.seen:
            return self.short_description
        else:
            self.seen=True
            return self.long_description

class Feature(GameObj):
    def __init__(self,**data):
        self.location=''
        self.seen=False
        self.alternate_names=[]
        self.canUnlock=False
        self.canUnhide=False
        self.__dict__.update(data)
    def __str__(self):
        if self.seen:
            return self.short_description
        else:
            self.seen=True
            return self.long_description
    
class Player(GameObj):
    def __init__(self,**data):
        self.items=[]
        self.location=''
        self.seen=False
        self.status='you are trying to win.'
        self.__dict__.update(data)

    def __str__(self):
        items=[itm.short_description for itm in self.items]
        inventory=','.join(items)
        if inventory=='':inventory="nothing"
        status='Status: %s'%self.status
        if self.seen:
            desc=self.short_description
##            return '%s\n%s\n%s'%(self.short_description,youhave,status)
        else:
            desc=self.long_description
            self.seen=True
##            return '%s\n%s\n%s'%(self.long_description,youhave,status)

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
        self.items+=[itemName]#add to our items
        room.items.remove(itemName)#remove from the room
        print 'You add the %s to your Inventory.'%itemName
        return True
    
    def dropItem(self,itemName):
        if not itemName in self.items:return False #we don't have the item
        if not self.location in self.otherObjects:return False #room is bad
        room=self.otherObjects[self.location]
        room.items+=[itemName]
        self.items.remove(itemName)
        return True

    def checkWin(self):
        '''checks to see if the game has been won'''
        if self.location=='engineering core' \
        and 'gold medallion' in self.items \
        and 'silver medallion' in self.items \
        and 'bronze medallion' in self.items:
            self.status='you have won the game!'
            print 'You have arrived at the engineering core with all the medallions.  You have won the game!'

    def move(self,direction):
        #test for the room
##       if not self.location in self.otherObjects:
##            return False
        #get the room
        ##remove clearScreens() if you don't like how it clears screen after moving to a new space
        room=self.otherObjects[self.location]
        #test for existence of direction in room.adjacent_rooms
        if not room.adjacent_rooms.has_key(direction):#is room in adjacent rooms?
            return False
        if direction in room.adjacent_rooms and direction not in room.lockedDirections:
            self.location = room.adjacent_rooms[direction]
            clearScreen()
            self.checkWin()
            return True
        elif direction in room.adjacent_rooms.itervalues() and direction not in room.lockedDirections:
            self.location = direction
            clearScreen()
            self.checkWin()
            return True
        #if bad, exit false
        else:
            clearScreen()
            self.checkWin()
            return False

    def unlockDirection(self,direction):
        #get the room
        room=self.otherObjects[self.location]
        #remove the lock
        room.lockedDirections.remove(direction)

    def unlockAllDirections(self):
        #get the room
        room=self.otherObjects[self.location]
        room.lockedDirections=[]

    def unhideAll(self):
        #get the room
        room=self.otherObjects[self.location]
        for item in room.items:
            obj=self.otherObjects[item]
            obj.hidden=False     

    def examine(self,itemName):
        if not self.location in self.otherObjects:
            return False

        adict=self.getNameAndAlternates()
        if not itemName in adict.keys():
            print "This room does not have that item!"
            return False

        realName=adict[itemName]
        item=self.otherObjects[realName]
##        if not isinstance(item,Item):
##            print "That is not an item!"
##            return False

        if hasattr(item,'canUnlock') and item.canUnlock==True:
            self.unlockAllDirections()
        if hasattr(item,'canUnhide') and item.canUnhide==True:
            self.unhideAll()
            
        
        t=item.type
        t.capitalize()
        print item.long_description
        #print '%s %s: %s'%(t, itemName,item.long_description)
        return True

    #need to implement use feature similar to examine object
    #or morph examine to handle use as well
    #if feature.canUnhide=True, must unhide all hidden items in the room
    #if item.canUnlock=True, must unlock all locked directions in the room


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
        clearScreen()
        phrases=["It feels as if you are swimming in a deep pool of warm water."]
        phrases+=["There are swirling lights and you are disoriented.  The bile is rising in your throat."]
        phrases+=["Your body feels as if it is being torn apart."]
        thephrase='You are teleporting to room %s!  %s\n'%(theroom,random.choice(phrases))
        self.location=theroom
        print thephrase
        return True

    def use(self, item, featureName, verb):
        room = self.otherObjects[self.location]
        feature = self.otherObjects[featureName]
        if not item in self.items:
            print 'You do not have that item'
            return False  # we don't have the item
        if not room.name in feature.location:
            print 'Feature is not in this room'
            return False #feature not in this room
        if not verb in feature.verb_use:
            print 'You cannot %s that'%verb
            return False
        if not item in feature.item_use:
            print 'You cannot use %s on %s' %(item, feature)
            return False
        else:
            print '%s' %feature.result_text
            feature.long_description = feature.description_change
            rItem = self.otherObjects[feature.result_item]
            rItem.hidden = 'false'
            self.getItem(rItem.name)
            return True


        
class Room(GameObj):
    def __init__(self,**data):
        self.items=[]
        self.features=[]
        self.adjacent_rooms={}
        self.visited=False
        self.lockedDirections=[]
        self.__dict__.update(data)

    def getDescriptions(self,alist):
        temp=[]
        for itmdesc in alist:
            if not self.otherObjects.has_key(itmdesc):
                print 'Room %s is missing item/feature %s!'%(self.name,itmdesc)
                continue
            itemobj=self.otherObjects[itmdesc]
            if not hasattr(itemobj,'short_description'):
                print 'The item %s is missing a short description.'%itmdesc
                continue
            temp+=[itemobj.short_description]
        return temp

    #returns an array of items (or features) that are available in a room
    def getList(self,alist):
        temp=[]
        for itmdesc in alist:
            if not self.otherObjects.has_key(itmdesc):
                print 'Room %s is missing item/feature %s!'%(self.name,itmdesc)
                continue
            itemobj=self.otherObjects[itmdesc]
            if not hasattr(itemobj,'name'):
                print 'The item %s is missing a name.'%itmdesc
                continue
            temp+=[itemobj.name]
        return temp
            
    def __str__(self):
        items=', '.join(self.getList(self.items))
        if items=='':items='nothing'
        features=', '.join(self.getList(self.features))
        if features=='':features='nothing'
        exits=sorted(self.adjacent_rooms.keys())
        exits=', '.join(exits)

##        if items:
##            itemsSee='In this room you see these items: %s'%', '.join(items)
##        else:
##            itemsSee='There are no items in this room.'
##
##        if features:
##            featuresSee='In this room you see these features: %s'%', '.join(features)
##        else:
##            featuresSee='There are no features in this room.'        

            
        if self.visited:
            desc=self.short_description
##            return '%s\n%s\n%s'%(self.short_description,itemsSee,featuresSee)
        else:
            desc=self.long_description
            self.visited=True
##            return '%s\n%s\n%s'%(self.long_description,itemsSee,featuresSee)

        h='>'*75
        thereturn='''
%s
Room name: %s
Room description: %s
Room features: %s
Room items: %s
Room exits: %s
%s
        '''%(h,self.name,desc,features,items,exits,h)
        return thereturn

#clears screen by adding 100 lines               
def clearScreen():
    print "\n" * 100