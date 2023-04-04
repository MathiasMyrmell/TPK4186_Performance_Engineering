
import sys
from decimal import *

class Action:
    def __init__(self, name, processTime, batch, buffer, task):
        self.name = name
        self.processTime = processTime
        self.batch = batch
        self.buffer = buffer
        self.task = task

        self.ongoing = False
        self.endTime = 0

    def isOngoing(self):
        return self.ongoing
    
    def canBeExecuted(self, currentTime):
        #Check if ongoing
        if self.ongoing:
            return False
        if self.name == "Load batch to 'Input buffer'":
            if self.buffer.canAcceptBatch(self.batch):
                return True
            else:
                return False
        elif self.name == "Load batch to task":
            #Check if task can accept batch
            if self.task.canAcceptBatch(self.batch, currentTime):
                return True
            else:
                return False
        elif self.name == "Load batch to buffer":
            #Check if buffer can accept batch
            if self.buffer.canAcceptBatch(self.batch):
                return True
            else:
                return False
                     
    def execute(self, currentTime):
        self.ongoing = True
        self.endTime = currentTime + round(Decimal(self.processTime),1)
        if(self.name == "Load batch to 'Input buffer'"):
            sys.stdout.write("{0:s}\t{1:s}\n".format(" ", self.getExecuteMessage()))
            self.buffer.add(self.batch, self.endTime)
        elif(self.name == "Load batch to task"):
            sys.stdout.write("{0:s}\t{1:s}\n".format(" ", self.getExecuteMessage()))
            self.task.startProduction(self.batch, self.endTime)
        elif (self.name =="Load batch to buffer"):
            sys.stdout.write("{0:s}\t{1:s}\n".format(" ", self.getExecuteMessage()))
            self.buffer.add(self.batch, self.endTime)
            

    def isFinished(self, currentTime):
        if currentTime >= self.endTime:
            return True
        else:
            return False
        
    def finish(self):
        # If next task is None, this action was loading to output buffer
        if self.task == None:
            return None
        else:# return next action
            if self.name == "Load batch to 'Input buffer'":
                name = "Load batch to task"
                processingTime = 1 #1 minute
                batch = self.batch #This batch
                buffer = self.buffer #Current buffer
                task = self.task #Next task
                processingTime += task.getProcessingTime()*batch.getNumWafers()#Add processing time of next task
                return Action(name, processingTime, batch, buffer, task)
            elif self.name == "Load batch to task":
                name = "Load batch to buffer"
                processingTime = 1 #1 minute
                batch = self.batch #This batch
                buffer = self.task.getNextBuffer() #Next buffer
                task = buffer.getNextTask() #No next task
                return Action(name, processingTime, batch, buffer, task)






    def getExecuteMessage(self):
        if self.name == "Load batch to 'Input buffer'":
            return "Loading batch to 'Input buffer'"
        elif self.name == "Load batch to task":
            return "Loading batch from "+str(self.buffer.name)+" to "+ str(self.task.name)
        elif self.name =="Load batch to buffer":
            return "Loading batch from "+str(self.task.name)+" to "+ str(self.buffer.name)

    def getFinishedMessage(self):
        if self.name == "Load batch to 'Input buffer'":
            return "Loaded batch to 'Input buffer'"
        elif self.name == "Load batch to task":
            return "Loaded batch from "+str(self.buffer.name)+" to "+ str(self.task.name)
        elif self.name =="Load batch to buffer":
            return "Loaded batch from "+str(self.task.name)+" to "+ str(self.buffer.name)