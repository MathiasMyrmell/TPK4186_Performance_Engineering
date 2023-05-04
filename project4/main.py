import openpyxl
from task import Task
from pert import PERT
import random
import copy

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
    # print("Number of projects: ", len(standardProjects))

    # Create 1000 random projects per risk factor
    projects = {}
    for r in riskFactors:
        projects[r] = []
    print(projects)
    for i in range(len(riskFactors)):
        base = standardProjects[i]
        print("Risk factor: ", riskFactors[i])
        for j in range(0,2):
            proj = copy.deepcopy(base)
            projNewDuration = _randomDuration(proj)
            executed = projNewDuration.executeProject()
            executed.getDuration()
            print(executed.finishTime)
            executed.printEarlyAndLateDates()
            projects[riskFactors[i]].append(executed)


    # for key, value in projects.items():
    #     print(key, value)
    #     for p in value:
    #         print(p.printEarlyAndLateDates())
    # projects = {}
    # for r in riskFactors:
    #     projects[r] = []
    # for i in range(0, len(riskFactors)):
    #     stdProj = standardProjects[i]
    #     proj = copy.deepcopy(stdProj)
    #     # print("Risk factor: ", riskFactors[i])
    #     # print(projects)
    #     for j in range(0,10):
    #         projNewDuration = _randomDuration(proj)
    #         # print(projNewDuration.getDurations())
    #         riskFactor = riskFactors[i]
    #         # print("a", projNewDuration)
    #         projects[riskFactor].append(projNewDuration.executeProject())
    # ## test executing one project
    # # p = projects[0]
    # # p.printEarlyAndLateDates()
    # factor8 = projects[0.8]
    # for p in factor8:
    #     # print(p)
    #     p.getDurations()

    # ## Classify projects
    # # classifyProjects(projects)

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



def classifyProjects(projects):
    for key, value in projects.items():
        print(value[0].finishTime)




if  __name__ == "__main__":
    # path = "project4/dataFiles/Villa.xlsx"
    path = "project4/dataFiles/Warehouse.xlsx"
    tasks = load(path)

    # # #Create Diagram
    # diagram = PERT(tasks)
    # # # Print the process plan
    # diagram.printProcessPlan()
    # # # Print early and late dates
    # diagram.printEarlyAndLateDates()

    task4(path)



    ####### Wrong middel time for task d in Warehouse? in task description it is 2 but in file it is 1
