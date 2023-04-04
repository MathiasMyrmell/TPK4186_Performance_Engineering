

class Unit:

    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def getName(self):
        return self.name

    def addTask(self, task):
        self.tasks.append(task)
    



        