import openpyxl
from task import Task
from pert import PERT

def load(path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    tasks = []
    for i in range(2, ws.max_row+1):
        type = ws.cell(row=i, column=1).value
        if type == None :
            continue
        id = i-1
        code = ws.cell(row=i, column=2).value
        description = ws.cell(row=i, column=3).value
        durations = ws.cell(row=i, column=4).value
        predecessorsStr = ws.cell(row=i, column=5).value

        #Get predecessors
        predecessors = []
        for t in tasks:
            if t.code in predecessorsStr:
                predecessors.append(t)

        task = Task(id, code, description, durations, predecessors)

        #Add new task as successor to its predecessors
        for t in tasks:
            if t in task.predecessors:
                t.successors.append(task)
        tasks.append(task)
    return tasks




if  __name__ == "__main__":
    path = "project4/dataFiles/Villa.xlsx"
    # path = "project4/dataFiles/Warehouse.xlsx"
    tasks = load(path)

    # #Create Diagram
    diagram = PERT(tasks)
    diagram.printer()
