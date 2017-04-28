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
        
class Room(GameObj):
    def __init__(self,**data):
        self.items=[]
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
            
        