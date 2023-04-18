from decimal import *

class Action:
        
        def __init__(self, name, batch, startTime, finishTime, inputbuffer = None, task = None, outputbuffer = None):
            # Initial values
            self.name = name
            self.batch = batch
            self.startTime = startTime
            self.finishTime = finishTime
            self.inputbuffer = inputbuffer
            self.task = task
            self.outputbuffer = outputbuffer
            # Production values
            self.nextAction = None
            self.status = False


        # #Getters
        # Returns next action
        def getNextAction(self):
            return self.nextAction
        
        # Returns name
        def getName(self):
            return self.name
        
        # Return batch
        def getBatch(self):
            return self.batch
        
        # Returns inputbuffer
        def getInputbuffer(self):
            return self.inputbuffer
        
        # Returns task
        def getTask(self):
            return self.task
        
        # Returns outputbuffer
        def getOutputbuffer(self):
            return self.outputbuffer
        
        # Returns status
        def getStatus(self):
            return self.status
        
        # Returns finish time
        def getFinishTime(self):
            return self.finishTime  

        # #Setters
        # Set next action
        def setNextAction(self, action):
            self.nextAction = action
        
        # Set Status
        def setStatus(self, status):
            self.status = status
        
        