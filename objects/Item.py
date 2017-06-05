##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.FeatureOrItem import FeatureOrItem

class Item(FeatureOrItem):
    def __init__(self,**data):
        super(Item,self).__init__()
        self.hidden=False
        self.__dict__.update(data)

if __name__=='__main__':
    itm=Item()
    print dir(itm)
