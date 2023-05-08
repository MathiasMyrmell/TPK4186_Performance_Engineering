import copy
from prettytable import PrettyTable
class Printer():

    def __init__(self, diagram = None):
        self.diagram = diagram

    def printProcessPlan(self):
        tasks = self.diagram.tasks
        earlyDates = self.diagram.earlyDates
        lateDates = self.diagram.lateDates
        criticality = self.diagram.criticality
        table = PrettyTable()
        table.field_names = ["Type","Code", "Description","Duration","Predecessors","Successors"]
        types = []
        codes = []
        descriptions = []
        durations = []
        predecessors = []
        successors = []


        for task in tasks:
            # Get type
            type = task.type
            types.append(type)
            # Get code
            code = task.code
            codes.append(code)
            # Get description
            description = task.getDescriptionStr()
            descriptions.append(description)
            # Get duration
            duration = task.getDurationStr()
            durations.append(duration)
            # Get predecessors
            predecessor = task.getPredecessorsStr()
            predecessors.append(predecessor)
            
            # Get successors
            successor = task.getSuccessorsStr()
            successors.append(successor)

            # Add to table
            table.add_row([type, code, description, duration, predecessor, successor])
        
        earlyStarts = [None]*len(codes)
        earlyFinishes = [None]*len(codes)
        lateStarts = [None]*len(codes)
        lateFinishes = [None]*len(codes)
        criticalities = [None]*len(codes)
        for task in earlyDates.keys():
            earlyStart = earlyDates[task][0]
            earlyFinish = earlyDates[task][1]
            lateStart = lateDates[task][0]
            lateFinish = lateDates[task][1]
            critical = ""
            if task in criticality:
                critical = "Yes"
            else:
                critical = "No"
            for i in range(len(codes)):
                if task.code == codes[i]:
                    earlyStarts[i] = earlyStart
                    earlyFinishes[i] = earlyFinish
                    lateStarts[i] = lateStart
                    lateFinishes[i] = lateFinish
                    criticalities[i] = critical
        table.add_column("Early Start", earlyStarts)
        table.add_column("Early Finish", earlyFinishes)
        table.add_column("Late Start", lateStarts)
        table.add_column("Late Finish", lateFinishes)
        table.add_column("Criticality", criticalities)
        print(table)

    def printEarlyAndLateDates(self):
        tasks = self.diagram.tasks
        earlyDates = self.diagram.earlyDates
        lateDates = self.diagram.lateDates
        # Get header row
        header = self._getHeaderRow(tasks)
        
        # convert results to table form
        tableRows = self._convertToTableForm(header, earlyDates, lateDates)
       
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


    
    def _convertToTableForm(self, header, earlyDates, lateDates):
        duration = []
        earlyStart = []
        earlyFinish = []
        lateStart = []
        lateFinish = []
        for code in header:
            for task, value in lateDates.items():
                if task.code == code:
                    if task.getDurations() == None:
                        duration.append(0)
                    else:
                        duration.append(task.getDuration())
                    earlyStart.append(earlyDates[task][0])
                    earlyFinish.append(earlyDates[task][1])
                    lateStart.append(lateDates[task][0])
                    lateFinish.append(lateDates[task][1])
        return [duration, earlyStart, earlyFinish, lateStart, lateFinish]



    ## Print test results
    # Classification
    def printClassification(self, res):
        print("result: ", res)

        for projectName, tests in res.items():
            table = PrettyTable()
            table.title = projectName
            table.field_names = ["Test", "Correct", "Wrong", "Accuracy"]
            for test, result in tests.items():
                correct = result[0]
                wrong = result[1]
                accuracy = result[0]/(result[0]+result[1])
                table.add_row([test, correct, wrong, accuracy])
            print(table)

