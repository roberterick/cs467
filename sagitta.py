##class: CS467
##group: Sagitta
##members: Robert Erick, James Wong, Brent Nolan
##date: 4/17/2017



import os
import json
import pickle

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
            self.loadGame()
        self.mainLoop()#begin main loop

    def mainLoop(self):
        while(1):
            #print descriptions
            a1=raw_input(">>>>")#prompt
            a1=a1.lower()
            if a1=='help':
                self.showHelp()
            elif a1=='save game':
                self.saveGame()
            elif a1=='load game':
                self.loadGame()
            elif a1=='exit':
                #implement exit, temp save if dirty?
                return
            elif a1=='print objects':
                self.printObjects()
            else:
                print 'That command is not recognized.'
                
                
            #analyze command
            
            
    def askNewGame(self):
        answer=raw_input('Start a new game?')
        return answer.lower()

    def showHelp(self):
        h='''
        save game: save the current game
        load game: load a saved game    
        exit: exit the game
        print objects: print known objects
        '''
        print h

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
        
    def loadGame(self):
        pth=os.path.join(self.where(),'saved')
        shortlist=os.listdir(pth)#file list without path
        if len(shortlist)==0:
            print 'No saved games found!'
            return
        shortlist.sort()
        for i,f in enumerate(shortlist):#display saved games
            print '%02i.'%i,f
        a1=raw_input('Choose game to load (an integer):')
        a1=a1.lower()
        longlist=[os.path.join(pth,x) for x in shortlist]#file list with path
        try:
            a1=int(a1)
        except:
            print 'Please enter an integer.'
            return
        target=longlist[i]
        fobj=open(target, 'rb')
        self.objs=pickle.load(fobj)
        fobj.close()

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
        pickle.dump(self.objs,fobj)
        fobj.close()
        
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

