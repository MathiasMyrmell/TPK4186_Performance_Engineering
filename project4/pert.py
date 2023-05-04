import copy
from prettytable import PrettyTable
from printer import Printer
class PERT:

    def __init__(self, tasks):
        self.tasks = tasks
        self.printer = Printer()

        # For executing project
        self.finishTime = 0


    def printProcessPlan(self):
        tasksCopy = copy.copy(self.tasks)
        self.printer.printProcessPlan(tasksCopy)

    def printEarlyAndLateDates(self):
        tasksCopy = copy.copy(self.tasks)
        self.printer.printEarlyAndLateDates(tasksCopy)
    
    def getFirstTask(self):
        for task in self.tasks:
            if task.predecessors == None:
                return task
        return None
    
    def getEndTask(self):
        return self.tasks[-1]

    def getTaskBycode(self, code):
        for task in self.tasks:
            if task.code == code:
                return task
        return None
    
    def getDurations(self):
        for task in self.tasks:
            print(task.getDurations())
    

    def executeProject(self):
        nodes = self.execute(self.tasks)
        finishTime = 0
        for key, value in nodes.items():
            if value[2]>finishTime:
                finishTime = value[2]
        self.finishTime = finishTime
        return self

   
    def execute(self, tasks):
        # key: task
        # value: [duration, earlyStart, earlyFinish]
        nodes = {}
        for task in tasks:
            if task.getDuration == None:
                nodes[task] = [0, None, None]
                continue
            nodes[task] = [task.getDuration(), None, None]
        startNode = self.getFirstTask(tasks)
        nodes[startNode] = [0,0,0]
        endNode = self.getEndTask(tasks)
        nodes[endNode] = [0,None,None]

        stopp = False
        while stopp == False:
            for node in nodes.keys():
                # print("--------------------")
                # If node is already calculated, continue with next node
                if nodes[node][1]!=None and nodes[node][2]!=None:
                    continue
                # Get predecessors
                predecessors = node.getPredecessors()
                # For each predecessor, get early startTimes
                earlyStartTimes = []

                # Check if all predecessors have earlyStart and earlyFinish. if not continue with next node
                break_flag = False
                for pre in predecessors:
                    if nodes[pre][2] == None:
                        print(node.code)
                        break_flag = True
                        break
                    else:
                        earlyStartTimes.append(nodes[pre][2])
                if break_flag:
                    continue

                # Get max earlyStartTime
                if len(earlyStartTimes) == 0:
                    maxEarlyStartTime = 0
                else:
                    maxEarlyStartTime = max(earlyStartTimes)
                # Get duration
                duration = nodes[node][0]
                # Calculate earlyFinishTime
                earlyFinishTime = round(maxEarlyStartTime + duration,3)
                # Set earlyStart and earlyFinish
                nodes[node][1] = maxEarlyStartTime
                nodes[node][2] = earlyFinishTime


                if nodes[endNode][1] != None and nodes[endNode][2] != None:
                    stopp = True

        return nodes

    
    def getFirstTask(self, tasks):
        for task in tasks:
            if len(task.predecessors) == 0:
                return task
        return None

    def getEndTask(self, tasks):
        for task in tasks:
            if len(task.successors) == 0:
                return task
        return None


    def getDuration(self):
        l = []
        for task in self.tasks:
            l.append(task.getDuration())

        print(l)