## Task 1

import copy
from prettytable import PrettyTable
from printer import Printer
class PERT:

    def __init__(self, name, tasks, riskFactor = 1):
        self.name = name
        self.riskFactor = riskFactor
        self.tasks = tasks
        self.printer = Printer()
        

        # For executing project
        self.finishTime = 0
        self.finishTimes = []
        self.earlyDates = None
        self.lateDates = None
        self.criticality = None
        self.projectClass = None

        # for machine learning
        self.intermediateGate = None


    ## Getters
    def getName(self):
        return self.name
    
    def getRiskFactor(self):
        return self.riskFactor
    
    def getTasks(self):
        return self.tasks
    
    def getFirstTask(self):
        for task in self.tasks:
            if len(task.predecessors) == 0:
                return task
        return None
    
    def getEndTask(self):
        return self.tasks[-1]

    def getTaskByCode(self, code):
        for task in self.tasks:
            if task.code == code:
                return task
        return None
    
    def getDurations(self):
        for task in self.tasks:
            # print(task.getDurations())
            pass

    # def getFirstTask(self, tasks):
    #     for task in tasks:
    #         if len(task.predecessors) == 0:
    #             return task
    #     return None

    def getEndTask(self, tasks):
        for task in tasks:
            if len(task.successors) == 0:
                return task
        return None

    def getDuration(self):
        l = []
        for task in self.tasks:
            l.append(task.getDuration())

        # print(l)

    def getIntermedateGate(self):
        return self.intermediateGate
    
    def getNumTasks(self):
        return len(self.tasks)



    ## Setters
    def setIntermediateGate(self, intermediateGate):
        self.intermediateGate = intermediateGate


    

    def __str__(self):
        return str(self.riskFactor)
    
    def __repr__(self):
        return self.__str__()

    def printProcessPlan(self):
        tasksCopy = copy.copy(self.tasks)
        self.printer.printProcessPlan(tasksCopy)

    def printEarlyAndLateDates(self):
        tasksCopy = copy.copy(self.tasks)
        self.printer.printEarlyAndLateDates(tasksCopy)
    

    def executeProject(self, duration):
        nodes = self.execute(duration)
        finishTimes = []
        for i in range(3):
            nodes = self.execute(i)
            finishTime = 0
            for key, value in nodes.items():
                if value[2]>finishTime:
                    finishTime = value[2]
            finishTimes.append(finishTime)
            self.calculateEarlyAndLateDates()
            self.calculateCriticality()
        self.finishTimes = finishTimes
        # return finishTime

   
    def execute(self, duration):
        # key: task
        # value: [duration, earlyStart, earlyFinish]
        tasks = copy.deepcopy(self.tasks)
        nodes = {}
        for task in tasks:
            if task.getDurations() == None:
                nodes[task] = [0, None, None]
                continue

            nodes[task] = [task.getDurations()[duration], None, None]
        startNode = self.getFirstTask()
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

    
    def calculateEarlyAndLateDates(self):
        self._calculateEarlyDates()
        self._calculateLateDates()


    def _calculateEarlyDates(self):
        nodes = {}
        tasks = self.tasks
        for task in tasks:
            if task.getDuration() == None:
                nodes[task] = [0, None, None]
                continue
            nodes[task] = [task.getDuration(), None, None]
        startNode = self.getFirstTask()
        nodes[startNode] = [0,0,0]
        
        endNode = self.getEndTask(tasks)
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
        
        self.earlyDates = nodes
    
    def _calculateLateDates(self):
        # key: task
        # value: [duration, earlyStart, earlyFinish, lateStart, lateFinish]
        tasks = self.earlyDates
        nodes = {}
        for key, value in tasks.items():
            nodes[key] = value+[None,None]
        startNode = self.getFirstTask()
        nodes[startNode] = [0,0,0,None,None]
        endNode = self.getEndTask(tasks)
        #Set late start and late finish for endNode to early start and early finish
        lateSaE = nodes[endNode][1]
        nodes[endNode][3] = lateSaE
        nodes[endNode][4] = lateSaE

        stopp = False
        while stopp == False:
            print("nodes",nodes)
            print("keys",nodes.keys())
            for task in reversed(nodes.keys()):
                print("code",task)
                node = self.getTaskByCode(task.code)
                print(node)
                if nodes[node][3]!=None and nodes[node][4]!=None:
                        continue
                # Get successors
                successors = node.getSuccessors()
                # For each successor, get late startTimes
                lateSTsuc = []
                for suc in successors:
                    lateSTsuc.append(nodes[suc][3])
                # Get min lateEndTime
                break_flag = False
                for suc in successors:
                    if nodes[suc][4] == None:
                        break_flag = True
                        break
                    else:
                        lateETsuc = nodes[suc][2]
                if break_flag:
                    continue
                lEndTime = min(lateSTsuc)

                #Calculate lateStartTime
                duration = nodes[node][0]
                lStartTime = round(lEndTime - duration,3)

                # Set lateStart and lateFinish
                nodes[node][3] = lStartTime
                nodes[node][4] = lEndTime
                if nodes[startNode][3] != None and nodes[startNode][4] != None:
                    stopp = True
        self.lateDates = nodes
        return nodes
    
    
    
    def calculateCriticality(self):
        # print("late",self._getLateDates())
        pass



    def getRows(self):
        tasks = copy.deepcopy(self.tasks)
        # Get header row
        header = self._getHeaderRow(tasks)
        # Caluclate early dates
        earlyDates = self._getEarlyDates(tasks)

        # Calculate late dates
        lateDates = self._getLateDates(earlyDates)
        # convert results to table form
        tableRows = self._convertToTableForm(header, lateDates)
       
        return header, tableRows


    def _getHeaderRow(self, tasks):
        header = []
        for task in tasks:
            header.append(task.code)
        return header

    def _getEarlyDates(self, tasks):
        # key: task
        # value: [duration, earlyStart, earlyFinish]
        nodes = {}
        for task in tasks:
            if task.getDuration() == None:
                nodes[task] = [0, None, None]
                continue
            nodes[task] = [task.getDuration(), None, None]
        startNode = self.getFirstTask(tasks)
        nodes[startNode] = [0,0,0]
        endNode = self.getEndTask(tasks)

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

    def _getLateDates(self, tasks):
        # key: task
        # value: [duration, earlyStart, earlyFinish, lateStart, lateFinish]
        nodes = {}
        for key, value in tasks.items():
            nodes[key] = value+[None,None]
        startNode = self.getFirstTask(tasks)
        nodes[startNode] = [0,0,0,None,None]
        endNode = self.getEndTask(tasks)
        #Set late start and late finish for endNode to early start and early finish
        lateSaE = nodes[endNode][1]
        nodes[endNode][3] = lateSaE
        nodes[endNode][4] = lateSaE

        stopp = False
        while stopp == False:
            for node in reversed(nodes.keys()):
                if nodes[node][3]!=None and nodes[node][4]!=None:
                        continue
                # Get successors
                successors = node.getSuccessors()
                # For each successor, get late startTimes
                lateSTsuc = []
                for suc in successors:
                    lateSTsuc.append(nodes[suc][3])
                # Get min lateEndTime
                break_flag = False
                for suc in successors:
                    if nodes[suc][4] == None:
                        break_flag = True
                        break
                    else:
                        lateETsuc = nodes[suc][2]
                if break_flag:
                    continue
                lEndTime = min(lateSTsuc)

                #Calculate lateStartTime
                duration = nodes[node][0]
                lStartTime = round(lEndTime - duration,3)

                # Set lateStart and lateFinish
                nodes[node][3] = lStartTime
                nodes[node][4] = lEndTime
                if nodes[startNode][3] != None and nodes[startNode][4] != None:
                    stopp = True

        return nodes
    
    
    def _convertToTableForm(self, header, lateDates):
        duration = []
        earlyStart = []
        earlyFinish = []
        lateStart = []
        lateFinish = []
        for i in range(len(header)):
            for key, value in lateDates.items():
                if key.code == header[i]:
                    duration.append(value[0])
                    earlyStart.append(value[1])
                    earlyFinish.append(value[2])
                    lateStart.append(value[3])
                    lateFinish.append(value[4])
        return [duration, earlyStart, earlyFinish, lateStart, lateFinish]

   
    # Shortest duration of all tasks
    def getShortestDuration(self):
        return self.finishTimes[0]
    
    # Expected duration of all tasks
    def getExpectedDuration(self):
        return self.finishTimes[1]
    # Longest duration of all tasks
    def getLongestDuration(self):
        return self.finishTimes[2]
