##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

class GameObj(object):
    def __init__(self):
        self.otherObjects=None
        self.long_description=''
        self.short_description=''
        
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
        room=self.objects[self.location]
        #add to room
        room.items+=[itemName]
        #remove item from my items
        self.items.remove(itemName)
        return True

    def move(self,direction):
        room=self.otherObjects[self.location]
        #test for existance of direction in room.adjacent_rooms
        # if found, adjust location, exit true
        if direction in room.adjacent_rooms:
           self.location = room.adjacent_rooms.direction
           return True
        elif direction in room.adjacent_rooms.itervalues():
            self.location = direction
            return True
        #if bad, exit false
        else: return False

        
class Room(GameObj):
    def __init__(self,**data):
        self.items=[]
        self.adjacent_rooms={}
        self.visited=False
        self.__dict__.update(data)
    def __str__(self):
        items=[itm.short_description for itm in self.items]
        if items:
            youhave='In this room you see these items: %s'%','.join(items)
        else:
            youhave='There are no items in this room.'
        if self.visited:
            return '%s\n%s'%(self.short_description,youhave)
        else:
            self.visited=True
            return '%s\n%s'%(self.long_description,youhave)
            
        
