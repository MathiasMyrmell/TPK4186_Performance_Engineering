

import sys
class Scheduler:

    def __init__(self):
        self.actions = []

    def addAction(self, action):
        self.actions.append(action)

    def updateActions(self, currentTime):
        for action in self.actions:
            actionFinished = False
            if action.isOngoing():
                actionFinished = action.isFinished(currentTime)
            if actionFinished:
                newAction = action.finish()
                if newAction != None:
                    self.actions.append(newAction)
                self.actions.remove(action)
                sys.stdout.write("{0:s}\t{1:s}\n".format(" ", action.getFinishedMessage()))


    def executeNewActions(self, currentTime):
        executedActions = []
        for action in self.actions:
            if action.canBeExecuted(currentTime):
                action.execute(currentTime)
                executedActions.append(action)
                self.actions.remove(action)
        for action in executedActions:
            self.actions.append(action)

        