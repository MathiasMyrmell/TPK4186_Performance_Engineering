
class Scheduler:
    
    def __init__(self):
        self.actions = []

    # # Getters
    # Returns actions
    def getActions(self):
        return self.actions
    
    # # Functions
    # Adds action to scheduler
    def addAction(self, action):
        self.actions.append(action)

    # Removes action from scheduler
    def removeAction(self, action):
        self.actions.remove(action)

    