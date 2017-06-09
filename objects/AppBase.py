##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017

import os
import json
import pickle
#import ply

from Feature import *
from FeatureOrItem import *
from GameObj import *
from Item import *
from Player import *
from Room import *
from Version import *

CURRENT_VERSION=1.2

class AppBase(object):
    def __init__(self):
        self.objects={}#dictionary holds rooms, the player, and items

    #clears screen by adding 100 lines
    def clearScreen(self):
        print "\n" * 100

    def where(self):return os.getcwd()

    def initializeGame(self):
        print 'Welcome to DEEP SPACE DERELICT'
        answer=raw_input('Start a new game (y/n)?')
        answer=answer.lower()
        if answer=='y':
            self.clearScreen()
            self.initializeFromJSONFiles()
        else:
            self.clearScreen()
            self.loadGame()

    def initializeFromJSONFiles(self):
        pth=os.path.join(self.where(),'init')
        nonjsonpath=os.path.join(self.where(),'init','not_json')
        shortlist=os.listdir(pth)#file list without path
        longlist=[os.path.join(pth,x) for x in shortlist]#file list with path
        longlist=filter(lambda x:os.path.isfile(x),longlist)
        for f in longlist:
            text=open(f,'r').read()#read in the text
            try:
                data=json.loads(text)#convert to json
            except:
                print '*'*10,'File %s has incorrect json.  Please correct!'%f
                continue

            self.loadFormattedText(nonjsonpath,data)
            
            if data['type']=='room':
                newobj=Room(**data)
            elif data['type']=='player':
                newobj=Player(**data)
            elif data['type']=='feature':
                newobj=Feature(**data)
            elif data['type']=='item':
                newobj=Item(**data)
            elif data['type']=='version':
                newobj=Version(**data)
            else:
                assert False #shouldn't happen
            name=newobj.name.lower()#insure that all names should be lower
            if hasattr(newobj,'adjacent_rooms'):
                for k,v in newobj.adjacent_rooms.items():
                    if not k==k.lower():print 'problem with adjacent roomf for %s'%name
            self.objects[name]=newobj#add the object to our dictionary
            newobj.otherObjects=self.objects#gives all objects access to other objects

        self.linkFeatures()
        self.linkItems()
        self.objects['version'].version=CURRENT_VERSION
##        print self.objects

    def linkItems(self):
        for k,v in self.objects.items():#items here means k,v pairs
            if v.type!='item':continue
            location=v.location
            if not self.objects.has_key(location) and self.objects[location]['type']=='room':
                print 'Item %s does not have a valid location!'%k
            room=self.objects[location]
            if not k in room.items: room.items+=[k]

    def linkFeatures(self):
        for k,v in self.objects.items():#items here means k,v pairs
            if v.type!='feature':continue
            location=v.location
            if not self.objects.has_key(location) and self.objects[location]['type']=='feature':
                print 'Feature %s does not have a valid location!'%k
            room=self.objects[location]
            if not k in room.items: room.features+=[k]

    def loadFormattedText(self,textpath,datadict):
        #this loads in values from an alternate text files
        #so that formatting is improved
        #the file must exist
        #the name must be the value in the key
        for k,v in datadict.items():
            if str(type(v)) not in ["<type 'unicode'>","<type 'str'>"]:continue
            fullpath=os.path.join(textpath,v)
            if os.path.exists(fullpath):datadict[k]=open(fullpath,'r').read() 

    def loadGame(self):
        pth=os.path.join(self.where(),'saved')
        shortlist,longlist=self.returnSanitizedLists(pth)
        if len(shortlist)==0:
            print 'No saved games found!  Starting a new game.'
            self.initializeFromJSONFiles()
            return

        for i,f in enumerate(shortlist):#display saved games
            print '%02i.'%i,f
        a1=raw_input('Choose game to load (an integer):')
        a1=a1.lower()
        
        try:
            a1=int(a1)
        except:
            print 'Please enter an integer.'
            return

        target=None
        try:
            target=longlist[a1]
        except:
            print 'Please enter an integer from 0 to %i'%len(longlist)-1
            return
        self.loadObjectsDict(target)

    def loadObjectsDict(self,apath):
        fobj=open(apath, 'rb')
        self.objects=pickle.load(fobj)
        fobj.close()

    def returnSanitizedLists(self,apath):
        shortlist=os.listdir(apath)#file list without path
        shortlist.sort()
        longlist=[os.path.join(apath,x) for x in shortlist]#file list with path
        for i in range(len(longlist)-1,-1,-1):
            target=longlist[i]

            with open(target, 'rb') as fobj:
                proposedObjects=None
                #see if a file is capable of loading
                try:
                    proposedObjects=pickle.load(fobj)
                except:
                    shortlist.pop(i)
                    longlist.pop(i)
                    continue
                #show only file containing the correct version
                if proposedObjects['version'].version!=CURRENT_VERSION:
                    shortlist.pop(i)
                    longlist.pop(i)
                    continue
        return shortlist,longlist

    def saveGame(self):
        answer=raw_input('Enter name to save:')
        answer=answer.lower()
        pth=os.path.join(self.where(),'saved','%s.pkl'%answer)
        #check if exists already
        if os.path.exists(pth):
            a2=raw_input('That file exists already. Overwrite (y/n)?')
            a2=a2.lower()
            if a2=='n':return
        fobj=open(pth, 'wb')
        pickle.dump(self.objects,fobj)
        fobj.close()


if __name__=='__main__':
    app=AppBase()
