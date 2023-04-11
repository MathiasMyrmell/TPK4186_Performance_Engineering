
import sys
from decimal import *
class Printer:
    def __init__(self, simulator, logger):

        self.simulator = simulator
        self.logger = logger



    # # Functions
    def printEvents(self, time):
        times = self.logger.getLog().keys()
        # print(time)
        # print(type(time))
        for t in times:
            if t == time:
                sys.stdout.write("\t"+str(time)+"\n")
                for event in self.logger.getLog()[t]: 
                    sys.stdout.write("\t   "+event+"\n")
    

    # Used for testing
    def getStatus(self):
        buffers = self.simulator.getProductionline().getBuffers()
        tasks = self.simulator.getProductionline().getTasks()
        actions = self.simulator.getScheduler().getActions()
        units = self.simulator.getProductionline().getUnits()
        batches = self.simulator.batches
        returnValue = "\n"
        for batch in batches:
            returnValue += str(batch.getNumWafers()) +", "
        returnValue += "\n"
        for action in actions:
            returnValue += action.getName() + ", finishTime: "+str(action.finishTime) +"\n"
        returnValue += "\n"
        for buffer in buffers:
            returnValue += buffer.getName() + ": " + str(buffer.currentLoad) + " wafers\n"
        returnValue += "\n"
        for task in tasks:
            returnValue += task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
        returnValue += "\n"
        for unit in units:
            returnValue += unit.getName() +"\n"
            for task in unit.getTasks():
                returnValue +="\t"+ task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
        returnValue+="Batches in system: "+str(len(batches))+"\n"

        sys.stdout.write(returnValue)

