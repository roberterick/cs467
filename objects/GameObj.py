##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

##import os
##import platform

class GameObj(object):
    def __init__(self):
        self.otherObjects=None
        self.long_description=''
        self.short_description=''
        self.name=''
        self.alternate_names=[]
        self.type=''
    def getPlayer(self):
        playerkey=filter(lambda x:self.otherObjects[x].type=='player',self.otherObjects.keys())[0]
        return self.otherObjects[playerkey]
    def clearScreen(self):
        print "\n" * 100

if __name__=='__main__':
    go=GameObj()
    print dir(go)
