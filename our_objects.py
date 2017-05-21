##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

class GameObj(object):
    def __init__(self):
        self.otherObjects=None
        self.long_description=''
        self.short_description=''
        self.name=''
        self.type=''

class Version(GameObj):
    def __init__(self,**data):
        self.version=0.0
        self.__dict__.update(data)       
        
class Item(GameObj):
    def __init__(self,**data):
        self.location=''
        self.seen=False
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
        self.__dict__.update(data)
    def __str__(self):
        items=[itm.short_description for itm in self.items]
        youhave='You have in your possession: %s'%','.join(items)
        if self.seen:
            return '%s\n%s'%(self.short_description,youhave)
        else:
            self.seen=True
            return '%s\n%s'%(self.long_description,youhave)

    def getItem(self,itemName):
        #verify room has the item
        if not self.location in self.otherObjects:return False
        room=self.objects[self.location]
        if not itemName in room.items:return False
        #get item
        if not self.otherObjects[itemName].__class__=='Item':return False
        self.items+=[itemName]
        #remove from room
        room.items.remove(itemName)
        return True
    
    def dropItem(self,itemName):
        #verify i have the item
        if not itemName in self.items:return False
        #find room    
        if not self.location in self.otherObjects:return False
        room=self.otherObjects[self.location]
        #add to room
        room.items+=[itemName]
        #remove item from my items
        self.items.remove(itemName)
        return True

    def move(self,direction):
        #test for the room
##       if not self.location in self.otherObjects:
##            return False
        #get the room
        room=self.otherObjects[self.location]
        #test for existance of direction in room.adjacent_rooms
##        if not room.adjacent_rooms.has_key(direction):
##            return False
        # if found, adjust location, exit true
##        self.location = room.adjacent_rooms[direction]
##        return True
        if direction in room.adjacent_rooms:
           self.location = room.adjacent_rooms[direction]
           return True
        elif direction in room.adjacent_rooms.itervalues():
            self.location = direction
            return True
        #if bad, exit false
        else: return False

    def examine(self,itemName):
        if not self.location in self.otherObjects:
            return False
        room=self.otherObjects[self.location]
        if (not itemName in room.items and not itemName in room.features):
            print "This room does not have that!"
            return False
        item=self.otherObjects[itemName]
        if itemName in room.items:
            print 'Item %s: %s'%(itemName,item.long_description)
        if itemName in room.features:
            print 'Item %s: %s'%(itemName,item.long_description)
        
class Room(GameObj):
    def __init__(self,**data):
        self.items=[]
        self.features=[]
        self.adjacent_rooms={}
        self.visited=False
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
        items=self.getList(self.items)
        features=self.getList(self.features)

        if items:
            itemsSee='In this room you see these items: %s'%', '.join(items)
        else:
            itemsSee='There are no items in this room.'

        if features:
            featuresSee='In this room you see these features: %s'%', '.join(features)
        else:
            featuresSee='There are no features in this room.'        

            
        if self.visited:
            return '%s\n%s\n%s'%(self.short_description,itemsSee,featuresSee)
        else:
            self.visited=True
            return '%s\n%s\n%s'%(self.long_description,itemsSee,featuresSee)
            
        
