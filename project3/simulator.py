
from productionline import Productionline
from batch import Batch
from unit import Unit
from task import Task
from buffer import Buffer

import sys
from decimal import *

class Action:
    def __init__(self, name, processTime, batch, buffer, task):
        self.name = name
        self.processTime = processTime
    #     self.progressTime = 0
        self.batch = batch
        self.buffer = buffer
        self.task = task
        self.ongoing = False
        self.finished = False
    #     self.nextAction = None
        self.completionTime = None

    def getName(self):
        return self.name
    
    def getFinished(self):
        return self.finished
    # def getCompletionTime(self):
    #     return self.completionTime

    def setCompletionTime(self,completionTime):
        self.completionTime = completionTime
    
    def canBePerformed(self):
        if(self.ongoing == True):
            return False
        elif(self.name == "Load batch to 'Input buffer'"):
            if(self.buffer.canAcceptBatch(self.batch) == False):
                return False
        

        return True


    #     if(self.ongoing == True):
    #         progressTime += Decimal(0.1)
    #         return False
    #     if(self.name == "Load batch from buffer to task"):
    #         #Check if next buffer can accept batch
    #         if(self.task.getNextBuffer().canAcceptBatch(self.batch, self.completionTime) == False):
    #             return False
    #         #Check if task is not busy
    #         elif(self.task.getInProduction() == True):
    #             return False
    #         else:
    #             self.task.startProduction(self.batch, self.completionTime)
    #             self.nextAction = Action("Load batch from task to buffer", 1, self.batch, self.task.getNextBuffer(), self.task)
    #         return True
    #     elif(self.name == "Load batch from task to buffer"):
    #         pass

class Scheduler:
    def __init__(self):
        self.actions = []


    def getActions(self):
        return self.actions
    
    def insertAction(self, action):
        self.actions.append(action)

    def isEmpty(self):
        return len(self.actions) == 0

    def removeAction(self, action):
        self.actions.remove(action)

    def popFirstAction(self):
        if self.isEmpty():
            return None
        return self.actions.pop(0)

class Simulator:
    def __init__(self, productionGoal):
        self.batches = self._createBatches(productionGoal)
        self.productionline = Productionline()
        self.scheduler = Scheduler()
        self.time = Decimal(0.0)
        # self.productionGoal = 0


    # Creating batches
    def _createBatches(self, numWafers):
        batches = []
        while(numWafers > 0):
            if(numWafers//50==0):
                batches.append(Batch(numWafers))
                numWafers = 0
            elif(numWafers//50 > 1):
                batches.append(Batch(50))
                numWafers -= 50
            elif(numWafers%50 == 0):
                batches.append(Batch(50))
                numWafers -= 50
            else:
                if(numWafers%50 < 20):
                    num = int(numWafers/2)
                    batches.append(Batch(num))
                    numWafers -= num
                else:
                    batches.append(Batch(50))
                    numWafers -= 50
        return batches
    
    def getTime(self):
        return round(self.time,1)
    
    # def setTime(self, time):
    #     self.time = time

    # def getProductionline(self):
    #     return self.productionline

    # def isFinished(self):
    #     return self.finished

    # def setProductionGoal(self, productionGoal):
    #     self.productionGoal = productionGoal

    def performAction(self, action):
        actionName = action.getName()
        if(actionName == "Load batch to 'Input buffer'"):
            #Calculate completion time
            completionTime = self.getTime() + action.processTime
            #Set completion time
            action.setCompletionTime(completionTime)
            #Set as ongoing
            action.ongoing = True
            #Add batch to buffer
            action.buffer.add(action.batch,completionTime)
            #Set as ongoing
            sys.stdout.write("{0:s}\t{1:s}\n".format(" ", "Loading batch to input buffer"))
            # #Create next action
            # newAction = Action("Load batch from 'Input buffer' to 'Task 1'", 1, action.batch, action.buffer, self.productionline.getTask("Task 1"))
            # self.scheduler.insertAction(newAction)
            # #Create log
            # act = "Loading batch from "+"'Input buffer'"+" to "+"'Task 1'"
            # sys.stdout.write("{0:f}\t{1:s}\n".format(self.getTime(),act))
        elif(actionName == "Load batch from buffer to task"):
            #Calculate completion time
            completionTime = self.getTime() + action.processTime
            #Set completion time
            action.setCompletionTime(completionTime)
            #Remove batch from buffer
            action.buffer.removeBatch(action.batch)
            #Set finish time for task
            action.task.setFinishTime(completionTime)
            #Set as ongoing
            sys.stdout.write("{0:s}\t{1:s}\n".format(" ", "Loading batch from buffer to task"))
            # #Create next action
            # newAction = Action("Load batch from task to buffer", 1, action.batch, action.buffer, action.task)
            # self.scheduler.insertAction(newAction)
            # #Create log
            # act = "Loading batch from "+"'"+action.task.getName()+"'"+" to "+"'"+action.buffer.getName()+"'"
            # sys.stdout.write("{0:s}\t{1:s}\n".format(" ",act))
        
        
        
        # if(actionName == "Load batch from buffer to task"):
        #     bufferName = action.buffer.getName()
        #     taskName = action.task.getName()
        #     act = "Loading batch from "+"'"+bufferName+"'"+" to "+"'"+taskName+"'"
        #     sys.stdout.write("{0:f}\t{1:s}\n".format(self.getTime(),act))
        # elif(actionName == "Load batch from task to buffer"):
        #     taskName = action.task.getName()
        #     bufferName = action.buffer.getName()
        #     act = "Loading batch from "+"'"+taskName+"'"+" to "+"'"+bufferName+"'"


    def createInitialLoadActionsForBatches(self):
        inputbuffer = self.productionline.getBuffer("Input buffer")
        for batch in self.batches:
            action = Action("Load batch to 'Input buffer'", 1, batch, inputbuffer, self.productionline.getTask("Task 1"))
            self.scheduler.insertAction(action)

    def checkScheduler(self):
        scheduler = self.scheduler
        for action in scheduler.actions:
            print(action.ongoing, action.canBePerformed())

            if action.getFinished():
                scheduler.removeAction(action)
            elif (not action.ongoing) and (action.canBePerformed()):
                self.performAction(action)


    def updateTime(self):
        print("Updating time")
        #Update time for tasks in production
        for task in self.productionline.getTasks():
            if task.getInProduction():
                task.elapsedTime += Decimal(0.1)



    def checkTasks(self):
        print("Checking tasks")
        for task in self.productionline.getTasks():
            #Check if task is in production
            if(task.getInProduction()):#Task in production
                #Check if batch is finished
                if task.checkIfBatchIsFinished(self.getTime()):
                    #Create new action for batch
                    newAction = Action("Load batch from task to buffer", 1, task.getBatch(), task.getBuffer(), task)
                    self.scheduler.insertAction(newAction)
            else:#Task not in production
                #Check if previous buffer is empty
                previousBuffer = task.getPreviousBuffer()
                if(previousBuffer.currentLoad == 0):
                    break
                #Check next buffer
                nextBuffer = task.getNextBuffer()
                if(nextBuffer.currentLoad == nextBuffer.maxCapacity):
                    break
                nextBufferCapacity = nextBuffer.maxCapacity - nextBuffer.currentLoad

                #Check if batch is finished loading
                for batch in previousBuffer.getBatches():
                    if(batch[1] >= self.getTime() and nextBufferCapacity>=batch[0].getNumWafers()):#<=
                        #Create new action for batch
                        newAction = Action("Load batch from buffer to task", 1, batch[0], previousBuffer, task)
                        self.scheduler.insertAction(newAction)
                        break
                


                



            # if(task.getInProduction()):
            #     task.checkIfBatchIsFinished(self.getTime())
            # else:
            #     previousBuffer = task.getPreviousBuffer()
            #     if(previousBuffer.currentLoad != 0):
            #         #Check if batch is finished loading
            #         for batch in previousBuffer.getBatches():
            #             if(batch[1] <= self.getTime()):
            #                 #Create new action for batch
            #                 newAction = Action("Load batch from buffer to task", 1, batch[0], previousBuffer, task)
            #                 self.performAction(newAction)
            #                 break



    def checkFinished(self):
        loadInOutputbuffer = self.productionline.getBuffer("Output buffer").currentLoad
        lastTaskRunning = self.productionline.getTask("Task 9").getInProduction()
        if(loadInOutputbuffer == self.productionGoal and not lastTaskRunning):
            return True

    def run(self):
        print("Running simulation...")
        self.createInitialLoadActionsForBatches()
        #Simulation loop
        # while not self.scheduler.isEmpty() or self.getTime() < 3:
        # while checkFinished():
        for i in range(20):
            # Init
            sys.stdout.write("{0:s}\t{1:s}\n".format(str(self.getTime()), "Actions performed"))

            #Check scheduler
            self.checkScheduler()

            # Update
            self.updateTime()

            #Check Tasks
            self.checkTasks()    

            print(self.productionline.getBuffer("Input buffer").currentLoad)



            # #Get action
            # action = None
            # #Check new actions
            # for i in range (len(self.scheduler.getActions())):
            #     act = self.scheduler.getActions()[i]
            #     if(act.canBePerformed()):
            #         action = self.scheduler.actions.pop(i)
            #         break
            # #Perform action
            # if(action != None):
            #     self.performAction(action)
               
            # # Check tasks
            # self.checkTasks()
            
            # #Check buffers
            # for buffer in self.productionline.getBuffers():
            #     if(buffer.currentLoad!=0):
            #         for batch in buffer.getBatches():
            #             #If bactch is finished loading to buffer
            #             if(batch[1]<=self.getTime()):
            #                 #Create new action for batch
            #                 newAction = Action("Load batch from buffer to task", 1, batch[0], buffer, buffer.nextTask)
            #                 self.scheduler.insertAction(newAction)
            #                 sys.stdout.write("{0:s}\t{1:s}\n".format("", "Started loading batch to "+buffer.nextTask.getName()))

            #Update IRL time
            self.time += Decimal(0.1)
            i+=1
            # Make every task go up 0.1 time units

                
                
        print("Simulation finished!")

if __name__ == "__main__":
    productionGoal = 50
    SIM = Simulator(productionGoal)
    # print("Batches:", SIM.batches)
    SIM.run()