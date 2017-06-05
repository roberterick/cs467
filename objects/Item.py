##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.FeatureOrItem import FeatureOrItem

class Item(FeatureOrItem):
    def __init__(self,**data):
        super(FeatureOrItem,self).__init__()
        self.hidden=False
        self.__dict__.update(data)
