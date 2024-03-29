## Task 1

import copy
from printer import Printer
class PERT:

    def __init__(self, name, tasks, riskFactor = 1):
        self.name = name
        self.riskFactor = riskFactor
        self.tasks = tasks
        self.printer = Printer(self)
        

        # For executing project
        self.finishTime = 0
        self.finishTimes = []
        self.earlyDates = None
        self.lateDates = None
        self.criticality = None
        self.projectClass = None
        self.expectedTime = None
        self.initialize()

        # for machine learning
        self.intermediateGate = None


    ### Getters
    def getName(self):
        return self.name
    
    def getTasks(self):
        return self.tasks
    
    def getFirstTask(self, tasks):

        for task in tasks:
            if len(task.predecessors) == 0:
                return task
        return None
    
    def getTaskByCode(self, code):
        for task in self.tasks:
            if task.code == code:
                return task
        return None
  
    def getEndTask(self, tasks):
        for task in tasks:
            if len(task.successors) == 0:
                return task
        return None

    def getEarlyDates(self):
        return self.earlyDates
    
    def getLateDates(self):
        return self.lateDates

    def getCriticality(self):
        return self.criticality

    def getExpectedTime(self):
        return self.expectedTime

    def getFinishTimes(self):
        return self.finishTimes
    
    def getProjectClass(self):
        return self.projectClass

    def getFinishTime(self):
        return self.finishTime


    ### Setters
    def setIntermediateGate(self, intermediateGate):
        self.intermediateGate = intermediateGate

    def setTasks(self, tasks):
        self.tasks = tasks

    
    ### Functions
    ## Initilaize project
    def initialize(self):
        nodes = self._execute()
        finishTimes = []
        for i in range(3):
            nodes = self._execute()
            finishTime = 0
            for key, value in nodes.items():
                if value[2]>finishTime:
                    finishTime = value[2]
            finishTimes.append(finishTime)
            self.calculateEarlyAndLateDates()
            self._calculateCriticality()
        self.finishTimes = finishTimes
        self.expectedTime = finishTimes[1]



    ### Task 3
    ## Calculate Early and late dates for the project
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
        startNode = self.getFirstTask(tasks)
        nodes[startNode] = [0,0,0]
        
        endNode = self.getEndTask(tasks)
        stopp = False
        
        while stopp == False:
            for node in nodes.keys():
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
        for task, value in nodes.items():
            late = value[1:]
            nodes[task] = late
        self.earlyDates = nodes
    
    def _calculateLateDates(self):
        tasks = self.earlyDates
        nodes = {}
        for key, value in tasks.items():
            nodes[key] = value+[None,None]
        startNode = self.getFirstTask(tasks)
        nodes[startNode] = [0,0,None,None]
        endNode = self.getEndTask(tasks)
        #Set late start and late finish for endNode to early start and early finish
        lateSaE = nodes[endNode][1]
        nodes[endNode][2] = lateSaE
        nodes[endNode][3] = lateSaE

        stopp = False
        while stopp == False:
            for task in reversed(nodes.keys()):
                node = self.getTaskByCode(task.code)
                if nodes[node][2]!=None and nodes[node][3]!=None:
                        continue
                # Get successors
                successors = node.getSuccessors()
                # For each successor, get late startTimes
                lateSTsuc = []
                for suc in successors:
                    lateSTsuc.append(nodes[suc][2])
                # Get min lateEndTime
                break_flag = False
                for suc in successors:
                    if nodes[suc][3] == None:
                        break_flag = True
                        break
                    else:
                        lateETsuc = nodes[suc][1]
                if break_flag:
                    continue
                lEndTime = min(lateSTsuc)

                #Calculate lateStartTime
                if node.getDuration() == None:
                    duration = 0
                else:
                    duration = node.getDurations()[1]
                lStartTime = round(lEndTime - duration,3)

                # Set lateStart and lateFinish
                nodes[node][2] = lStartTime
                nodes[node][3] = lEndTime
                if nodes[startNode][2] != None and nodes[startNode][3] != None:
                    stopp = True
        for task, value in nodes.items():
            late = value[2:]
            nodes[task] = late
        self.lateDates = nodes
        return nodes
    


    ## Execute project
    # Runs trough the grapg and calculates data
    def executeProject(self):
        nodes = self._execute()
        finishTime = 0
        for key, value in nodes.items():
            if value[2]>finishTime:
                finishTime = value[2]
        self.finishTime = finishTime
   
    def _execute(self):
        tasks = self.tasks
        nodes = {}
        for task in tasks:
            if task.getDurations() == None:
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


    # Sets critical tasks
    def _calculateCriticality(self):
        criticality = []
        for task, value in self.earlyDates.items():
            earlyStart = value[0]
            lateStart = self.lateDates[task][0]
            isStart = task.isStartTask()
            isEnd = task.isEndTask()
            if earlyStart == lateStart and not isStart and not isEnd:
                criticality.append(task)
        self.criticality = criticality

    # Return early and late days table
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
            header.append(task.getCode())
        return header

    def _getEarlyDates(self, tasks):
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
            for task, value in lateDates.items():
                if task.getCode() == header[i]:
                    duration.append(value[0])
                    earlyStart.append(value[1])
                    earlyFinish.append(value[2])
                    lateStart.append(value[3])
                    lateFinish.append(value[4])
        return [duration, earlyStart, earlyFinish, lateStart, lateFinish]

   
    ### For printing
    def printProcessPlan(self):
        self.printer.printProcessPlan()

    def printEarlyAndLateDates(self):
        self.printer.printEarlyAndLateDates()
    
    ### Representation
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()