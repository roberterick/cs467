##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017



import os
import json

class GameObj(object):
    def __init__(self,**data):
        self.__dict__.update(data)
    
class App(object):
    def __init__(self):
        print 'initializing'
        self.objs={}#dictionary holds rooms, the player, and items

        if self.askNewGame()=='y':
            self.initializeFromFiles()
        else:
            self.loadSavedGame()

        self.printObjects()
            
    def askNewGame(self):
        answer=raw_input('Start a new game?')
        return answer.lower()

    def where(self):
        return os.getcwd()

    def initializeFromFiles(self):
        pth=os.path.join(self.where(),'init')
        shortlist=os.listdir(pth)#file list without path
        longlist=[os.path.join(pth,x) for x in shortlist]#file list with path
        for f in longlist:
            text=open(f,'r').read()#read in the text
            data=json.loads(text)#convert to json
            newobj=GameObj(**data)#create the obj with all json keys & data
            self.objs[newobj.name]=newobj#add the object to our dictionary
##        print self.objs
        
    def loadSavedGame(self):
##        display saved games
##        load saved games
        pass

    def printObjects(self):
        '''helper function to see what is there'''
        for k in self.objs:
            for k2 in dir(self.objs[k]):
                if not k2.startswith('_'):
                    print k2,':',eval('self.objs[k].%s'%k2)
            print




if __name__ == "__main__":
    app=App()
    print app.where()

