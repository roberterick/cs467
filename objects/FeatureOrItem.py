##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.GameObj import GameObj

class FeatureOrItem(GameObj):
    def __init__(self):
        super(FeatureOrItem,self).__init__()
        self.location=''
        self.seen=False
        self.canUnlock=False
        self.canUnhide=False
    def __str__(self):
        if self.seen:
            return self.short_description
        else:
            self.seen=True
            return self.long_description
    def unlockAllDirections(self):
        if not self.canUnlock:return False
        #get the player
        player=self.getPlayer()
        #get the location
        location=player.location
        #get the room
        room=self.otherObjects[location]
        #unlock all directions
        room.locked_directions=[]
        print "All directions in this room have been unlocked!"
        return True
    def unhideAllItems(self):
        if not self.canUnhide:return False
        #get the player
        player=self.getPlayer()
        #get the location
        location=player.location
        #get the room
        room=self.otherObjects[location]
        for item in room.items:
            obj=self.otherObjects[item]
            obj.hidden=False
        return True
    
##    def unlockDirection(self,unlockroomDirection):
##        unlockroom,direction=unlockroomDirection
##        #get the player
##        player=self.getPlayer()
##        #get the location
##        location=player.location
##        if not unlockroom==location:
##            print 'This item cannot unlock %s in this room!'%direction
##            return False
##        #get the room
##        room=self.otherObjects[location]
##        #unlock direction
##        while(direction in room.locked_directions):
##            room.locked_directions.remove(direction)
##        print 'The item has unlocked direction %s in this room!'%direction
##        return True

if __name__=='__main__':
    foi=FeatureOrItem()
    print dir(foi)
