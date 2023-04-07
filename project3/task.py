
from buffer import Buffer
from decimal import *
class Task: 

    def __init__(self,id, name, processingTime):
        #Initial values
        self.id = id
        self.name = name
        self.processingTime = processingTime
        #Production values
        self.inputbuffer = None
        self.outputbuffer = None
        self.unit = None
        self.inProduction = False
        self.batch = None
        self.startTime = 0
        self.elapsedTime = 0
        self.finishTime = 0

    # #Getters
    # Returns id
    def getId(self):
        return self.id
    
    # Returns name
    def getName(self):
        return self.name
    
    # Returns input buffer
    def getInputbuffer(self):
        return self.inputbuffer

    # Returns output buffer
    def getOutputBuffer(self):
        return self.outputbuffer

    # Returns unit
    def getUnit(self):
        return self.unit
   
    # Returns if task is in production or not
    def getInProduction(self):
        return self.inProduction
    

    # #Setters
    # Set input buffer
    def setInputbuffer(self, buffer):
        buffer.setNextTask(self)
        self.inputbuffer = buffer
    
    # Set output buffer
    def setOutputBuffer(self, buffer):
        buffer.setPreviousTask(self)
        self.outputbuffer = buffer
    
    # Set unit
    def setUnit(self, unit):
        self.unit = unit

    # Set in production
    def setInProduction(self, inProduction):
        self.inProduction = inProduction


    # #Functions
    # Returns processing time for given batch
    def calculateProcessingTime(self, batch):
        #Calculate total time
        totWafers = batch.getNumWafers()
        totTime = round(Decimal(self.processingTime * totWafers),1)
        return totTime

    # End production in task
    def endProduction(self):
        self.inProduction = False
        self.batch = None
        self.finishTime = 0
        self.elapsedTime = 0
        self.unit.setInProduction(False)

    # Checks if task can accept batch
    def canAcceptBatch(self, batch):
        #Check if task is not busy
        if(self.getInProduction() == True):
            return False
        #Check if next buffer can´t accept batch
        elif(self.getOutputBuffer().canAcceptBatch(batch) == False):
            return False
        #Check if a task in the unit is running
        elif(self.getUnit().getInProduction() == True):
            return False
        else:
            return True












    # def startProduction(self, batch, startTime):
    #     self.batch = batch
    #     self.inProduction = True
    #     self.finishTime = round(Decimal(self.getTotalTime()),1)+startTime
    #     self.unit.setInProduction(True)
    #     return self.finishTime

    # def startProduction(self, startTime):
    #     for batch in self.inputbuffer.getBatches():
    #         if self.canAcceptBatch(batch):
    #             pass




    #         # print("Batch ",batch.id)
    #         # if(self.canAcceptBatch(batch)):
    #         #     self.batch = batch
    #         #     self.inProduction = True
    #         #     self.finishTime = round(Decimal(self.getTotalTime()),1)+startTime
    #         #     self.unit.setInProduction(True)
    #         #     return self.finishTime

    # def getProcessingTime(self):
    #     return self.processingTime
    
    # def getInputbuffer(self):
    #     return self.inputbuffer
    
    # def getTotalTime(self):
    #     #Calculate total time
    #     totWafers = self.batch.getNumWafers()
    #     totTime = self.processingTime * totWafers
    #     return totTime
    
















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
   
