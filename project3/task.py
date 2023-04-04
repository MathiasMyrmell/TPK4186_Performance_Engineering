
from buffer import Buffer
from decimal import *
class Task: 

    def __init__(self, name, processingTime):
        #General info
        self.name = name
        self.processingTime = processingTime
        self.previousBuffer = None
        self.nextBuffer = None
        #Production info
        self.inProduction = False
        self.batch = None
        self.startTime = 0
        self.elapsedTime = 0
        self.finishTime = 0



    def getName(self):
        return self.name
    
    # def getProcessingTime(self):
    #     return self.processingTime
    
    def setPreviousBuffer(self, buffer):
        buffer.setNextTask(self)
        self.previousBuffer = buffer
    
    def getPreviousBuffer(self):
        return self.previousBuffer
    
    def setNextBuffer(self, buffer):
        buffer.setPreviousTask(self)
        self.nextBuffer = buffer
    

    def getNextBuffer(self):
        return self.nextBuffer

    def getInProduction(self):
        return self.inProduction
    

    def getTotalTime(self):
        #Calculate total time
        totWafers = self.batch.getNumWafers()
        totTime = self.processingTime * totWafers
        return totTime
   
    def startProduction(self, batch, startTime):
        self.batch = batch
        self.inProduction = True
        self.finishTime = round(Decimal(self.getTotalTime()),1)+startTime
        return self.finishTime

    def endProduction(self):
        self.inProduction = False
        self.batch = None
        self.finishTime = 0
        self.elapsedTime = 0


    def canAcceptBatch(self, batch):
        #Check if task is not busy
        if(self.getInProduction() == True):
            return False
        #Check if next buffer can´t accept batch
        elif(self.getNextBuffer().canAcceptBatch(batch) == False):
            return False
        else:
            return True

    # def setInProduction(self, inProduction):
    #     self.inProduction = inProduction

    # def setStartTime(self, startTime):
    #     self.startTime = startTime

    # def getTimeLeft(self):
    #     #Calculate total time
    #     totWafers = self.batch.getNumWafers()
    #     totTime = self.processingTime * totWafers
    #     #Time elapsed
    #     timeElapsed = self.elapsedTime
    #     #Time left
    #     timeLeft = totTime - timeElapsed
    #     return timeLeft

        # def setFinishTime(self, finishTime):
    #     self.finishTime = finishTime
   
