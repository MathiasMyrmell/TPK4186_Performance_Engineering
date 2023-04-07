
import sys

class Printer:
    def __init__(self, simulator):
        self.simulator = simulator


    def getStatus(self):
        buffers = self.simulator.productionline.getBuffers()
        tasks = self.simulator.productionline.getTasks()
        actions = self.simulator.scheduler.getActions()
        units = self.simulator.productionline.getUnits()
        returnValue = "\n"
        print("Actions: ", len(actions))
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
            returnValue += unit.name +"\n"
            for task in unit.tasks:
                returnValue +="\t"+ task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
        sys.stdout.write(returnValue)


    
