##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.GameObj import GameObj

class Version(GameObj):
    def __init__(self,**data):
        super(GameObj,self).__init__()
        self.version=0.0
        self.__dict__.update(data)
