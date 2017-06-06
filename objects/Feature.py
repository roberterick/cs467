##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.FeatureOrItem import FeatureOrItem

class Feature(FeatureOrItem):
    def __init__(self,**data):
        super(Feature,self).__init__()
        self.verb_use=[]
        self.item_use=[]
        self.description_change=''
        self.result_item=None
        self.destroy_item=False
        self.__dict__.update(data)

if __name__=='__main__':
    f=Feature()
    print dir(f)
