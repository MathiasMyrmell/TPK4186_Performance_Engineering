import copy
from prettytable import PrettyTable
class Printer():

    def __init__(self):
        pass

    def printProcessPlan(self, tasks):
        table = PrettyTable()
        table.field_names = ["Type","Code", "Description","Duration","Predecessors","Successors"]
        for task in tasks:
            # Get type
            type = task.type
            # Get code
            code = task.code
            # Get description
            description = task.getDescriptionStr()
            # Get duration
            duration = task.getDurationStr()
            # Get predecessors
            predecessor = task.getPredecessorsStr()
            
            # Get successors
            successor = task.getSuccessorsStr()
            # Add to table
            table.add_row([type, code, description, duration, predecessor, successor])

        print(table)

    def printEarlyAndLateDates(self, tasks):
        # Get header row
        header = self._getHeaderRow(tasks)
        # Caluclate early dates
        earlyDates = self._getEarlyDates(tasks)

        # Calculate late dates
        lateDates = self._getLateDates(earlyDates)
        # convert results to table form
        tableRows = self._convertToTableForm(header, lateDates)
       
        # Print table
        table = PrettyTable()
        table.field_names = ["Task"]+header
        column_names = ["Duration","Early Start", "Early Finish", "Late Start", "Late Finish"]
        for row in range(len(tableRows)):
            table.add_row([column_names[row]] + tableRows[row])
        print(table)

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
            if task.getDurations() == None:
                nodes[task] = [0, None, None]
                continue
            nodes[task] = [task.getDurations()[1], None, None]
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



