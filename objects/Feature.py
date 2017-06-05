##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.FeatureOrItem import FeatureOrItem

class Feature(FeatureOrItem):
    def __init__(self,**data):
        super(FeatureOrItem,self).__init__()
        self.__dict__.update(data)
