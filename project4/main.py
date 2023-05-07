import openpyxl
from task import Task
from pert import PERT
from machineLearning import ML
import random
import copy
from sklearn import svm

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


## Machine learning
def task4(path):
    standardProjects = []
    # # Calculate new durations
    riskFactors = [0.8,1.0,1.2,1.4]
    for factor in riskFactors:
        # print("Risk factor: ", factor)
        tasks = load(path)
        for task in tasks:
            duration = task.getDurations()
            # print("oldDuration",duration)
            newDuration = _calculateNewDuration(duration, factor)
            # print("newDuration",newDuration)
            task.setDurations(newDuration)

        #Create Diagram

        diagram = PERT(tasks)
        # diagram.printEarlyAndLateDates()
        # diagram.getDurations()
        standardProjects.append(diagram)

    # Standard time for project for each risk factor
    # expectedRunningTime = {}
    # for p in range(len(riskFactors)):
    #     demo = copy.deepcopy(standardProjects[p])
    #     finishTime = demo.executeProject().finishTime
    #     # print(finishTime)
    #     expectedRunningTime[riskFactors[p]] = finishTime

    # print("Expected running time: ", expectedRunningTime)

    # Create 1000 random projects per risk factor
    projects = {}
    for r in riskFactors:
        projects[r] = []
    # print(projects)
    for i in range(len(riskFactors)):
        base = standardProjects[i]
        # print("Risk factor: ", riskFactors[i])
        for j in range(0,1000):#
            proj = copy.deepcopy(base)
            projNewDuration = _randomDuration(proj)
            executed = projNewDuration.executeProject()
            # executed.getDuration()
            # print(executed.finishTime)
            executed.printEarlyAndLateDates()
            projects[riskFactors[i]].append(executed)

    # factor8 = projects[0.8]
    # for p in factor8:
    #     # print(p)
    #     p.getDurations()


    # Classify projects
    classifyProjects(projects)

def _calculateNewDuration(duration, factor):
    newDuration = []
    if(type(duration) != list):
        return duration
    newExpected = round(duration[1]*factor,3)
    oldMinimum = duration[0]
    oldExpected = duration[1]
    oldMaximum = duration[2]
    if(newExpected<oldMinimum):
        newDuration = [newExpected, oldExpected, oldMaximum]
    elif(newExpected>oldMaximum):
        newDuration = [oldMinimum, oldExpected, newExpected]
    else:
        newDuration = [oldMinimum, newExpected, oldMaximum]
    return newDuration


def _randomDuration(proj):
    project = copy.deepcopy(proj)
    tasks = project.tasks
    for task in tasks:
        if task.getDurations() == None:
            continue
        else:
            selectedDuration = random.choice(task.getDurations())
            task.setDuration(selectedDuration)
    return project



def classifyProjects(projects,):
    classification = {"Successfull": [], "Acceptable": [], "Failed": []}
    for key, value in projects.items():
        for p in value:
            eFinishTime = p.expectedTime
            finishTime = p.finishTime
            factor = finishTime/eFinishTime
            if factor <1.05:
                classification["Successfull"].append(p)
            elif factor <1.15:
                classification["Acceptable"].append(p)
            else:
                classification["Failed"].append(p)
    for key, value in classification.items():
        print(key, len(value))#, value)



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
    diagram.executeProject(1)
    # # #Calculate durations
    # finishTimes = diagram.calculateFinishTimes()
    print("For ",diagram.getName(), " the finish times is: \n Shortest: ", diagram.getShortestDuration(), "\n Expected: ", diagram.getExpectedDuration(), "\n Longest: ",diagram.getLongestDuration())

    # # print early dates of p
    print("earlyDates", diagram.earlyDates)
    print("lateDates", diagram.lateDates)






    # # Print the process plan
    # diagram.printProcessPlan()
    # # # # Print early and late dates
    # diagram.printEarlyAndLateDates()

    # task4(path)



    ####### Wrong middel time for task d in Warehouse? in task description it is 2 but in file it is 1




    # ## #Machine learning
    # # Create machine learning object
    # ml = ML()
    # # Load data
    # ml.loadFile(pathW)
    # ml.loadFile(pathV)

    # ## Preprocess data
    # ml.preprocessData()

    # ## Add gates to each project
    # ml.addIntermediateGates("Warehouse", "F")
    # ml.addIntermediateGates("Villa", "F.1")

    # ## Create set of data for Classification and Regression
    # learningTestData = ml.createInstancesDataClassification()
    # # print("learningTestDataMain",learningTestData)


    # ## Perform classification
    # # ml.classification(learningTestData)

    # ## Perform regression
    # ml.regression(learningTestData)

