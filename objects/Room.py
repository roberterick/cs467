##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017
from objects.GameObj import GameObj

class Room(GameObj):
    def __init__(self,**data):
        super(Room,self).__init__()
        self.items=[]
        self.features=[]
        self.adjacent_rooms={}
        self.visited=False
        self.locked_directions=[]
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
    def getList(self,alist,visibleOnly=True):
        temp=[]
        for itmdesc in alist:
            if not self.otherObjects.has_key(itmdesc):
                print 'Room %s is missing item/feature %s!'%(self.name,itmdesc)
                continue
            itemobj=self.otherObjects[itmdesc]
            if not hasattr(itemobj,'name'):
                print 'The item %s is missing a name.'%itmdesc
                continue
            if visibleOnly and hasattr(itemobj,'hidden') and itemobj.hidden:
                continue
            temp+=[itemobj.name]
        return temp
        
            
    def __str__(self):
        items=', '.join(self.getList(self.items,visibleOnly=True))
        if items=='':items='nothing'
        features=', '.join(self.getList(self.features,visibleOnly=True))
        if features=='':features='nothing'
        exits=sorted(['%s to %s'%(k,v) for k,v in self.adjacent_rooms.items()])
##        exits=sorted(self.adjacent_rooms.keys())
        exits=', '.join(exits)

##        if items:
##            itemsSee='In this room you see these items: %s'%', '.join(items)
##        else:
##            itemsSee='There are no items in this room.'
##
##        if features:
##            featuresSee='In this room you see these features: %s'%', '.join(features)
##        else:
##            featuresSee='There are no features in this room.'        

            
        if self.visited:
            desc=self.short_description
##            return '%s\n%s\n%s'%(self.short_description,itemsSee,featuresSee)
        else:
            desc=self.long_description
            self.visited=True
##            return '%s\n%s\n%s'%(self.long_description,itemsSee,featuresSee)

        h='>'*75
        thereturn='''
%s
Room name: %s
Room description: %s
Room features: %s
Room items: %s
Room exits: %s
%s
        '''%(h,self.name,desc,features,items,exits,h)
        return thereturn





if __name__=='__main__':
    r=Room()
    print dir(r)
