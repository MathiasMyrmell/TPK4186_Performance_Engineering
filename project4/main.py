import openpyxl
from task import Task
from pert import PERT
from machineLearning import ML
import random
import copy
from sklearn import svm

# # Task 2
## Load tasks from excel file
def load(path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    tasks = []
    for i in range(2, ws.max_row+1):
        id = i-1
        type = ws.cell(row=i, column=1).value
        if type == None :
            continue
        
        code = ws.cell(row=i, column=2).value
        description = ws.cell(row=i, column=3).value
        durations = ws.cell(row=i, column=4).value
        task = Task(id, type, code, description, durations)

        tasks.append(task)
    # Add predecessors and successors
    _addPreAndSuc(tasks, wb)        
    return tasks


def _addPreAndSuc(tasks, wb):
    ws = wb.active
    # Add predecessors
    for i in range(2, ws.max_row+1):
        type = ws.cell(row=i, column=1).value
        if type == None :
            continue
        for task in tasks:
            code = ws.cell(row=i, column=2).value
            predecessors = []
            successors = []
            if task.code == code:
                # print("Code: ", code)
                # Add predecessors
                predecessorsStr = ws.cell(row=i, column=5).value
                if predecessorsStr == None:
                    continue
                else:
                    predecessorsStr = predecessorsStr.replace(" ", "").split(",")
                for pre in predecessorsStr:
                    for t in tasks:
                        if t.code == pre:
                            predecessors.append(t)
                task.setPredecessors(predecessors)

    # Add successorts
    for t in tasks:
        # Find predeccsors to task
        for pre in t.predecessors:
            # for each predeccesor, add task as successor
            for task in tasks:
                if task.code == pre.code:
                    task.successors.append(t)



if  __name__ == "__main__":
    Path_V = "project4/dataFiles/Villa.xlsx"
    Path_W = "project4/dataFiles/Warehouse.xlsx"
    Tasks_V = load(Path_V)
    Tasks_W = load(Path_W)


    # # #Task 1
    print("--------------------Task 3--------------------")
    # # #Create diagram
    diagram = PERT("Test Project", Tasks_W)
    # # #Execute project
    diagram.executeProject()

    # print early dates of p
    print("earlyDates", diagram.earlyDates)
    print("lateDates", diagram.lateDates)

    # Print the process plan
    diagram.printProcessPlan()
    # # # # Print early and late dates
    diagram.printEarlyAndLateDates()


    ## #Machine learning
    # # Task 4
    print("--------------------Task 4--------------------")

    # # # Create machine learning object
    ml = ML()
    # # Load data
    ml.loadFile(Path_V)
    ml.loadFile(Path_W)

    # ## Preprocess data
    ml.preprocessData()

    # # Task 5
    print("--------------------Task 5--------------------")
    # ## Add gates to each project
    ml.addIntermediateGates("Warehouse", "F")
    ml.addIntermediateGates("Villa", "Q.1")

    # # ## Create set of data for Classification and Regression
    learningTestData = ml.createInstancesDataClassification()
    # # ## Perform classification
    res = ml.classification(learningTestData)
    ml.printClassification(res)

    # # Task 6
    print("--------------------Task 6--------------------")
    # # ## Perform regression
    resReg = ml.regression(learningTestData)
    ml.printRegression(resReg)

