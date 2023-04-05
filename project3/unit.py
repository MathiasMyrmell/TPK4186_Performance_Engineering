

class Unit:

    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.inProduction = False
    
    def getName(self):
        return self.name

    def addTask(self, task):
        task.setUnit(self)
        self.tasks.append(task)

    
    def setInProduction(self, inProduction):
        self.inProduction = inProduction

    def getInProduction(self):
        return self.inProduction



        