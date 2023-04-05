

class Unit:

    def __init__(self, name, heuristic):
        self.name = name
        self.tasks = []
        self.inProduction = False
        self.heuristic = heuristic
    
    def getName(self):
        return self.name

    def addTask(self, task):
        task.setUnit(self)
        self.tasks.append(task)

    
    def setInProduction(self, inProduction):
        self.inProduction = inProduction

    def getInProduction(self):
        return self.inProduction




    # # Task 5
    def startProduction(self, startTime):
        for id in self.heuristic:
            task = self._getTaskById(id)
            print(task.getName())
            if task != None:
                startedProduction = task.startProduction2(startTime)
                if startedProduction:
                    self.inProduction = True
                    return True

    def _getTaskById(self, id):
        for task in self.tasks:
            if task.id == id:
                return task
        return None
        