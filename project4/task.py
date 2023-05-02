

class Task:

    def __init__(self, id, code, description, durations, predecessors):
        self.id = id
        self.code = code
        self.description = description
        self.duration = self._durations(durations)
        self.predecessors = self._predecessors(predecessors)
        self.successors = []

    
    def getDuration(self):
        return self.duration[1]
    
    def getEarlyDuration(self):
        return self.duration[0]
    
    def getLateDuration(self):
        return self.duration[2]
    
    def getPredecessors(self):
        return self.predecessors

    # Change format from string to list
    def _durations(self, durations):
        returnValue = []
        if type(durations) != str:
            return durations
        durations = durations.replace('(', '').replace(')', '').replace(' ','').split(",")
        for i in durations:
            i = int(i)
            returnValue.append(i)
        return returnValue

    def _predecessors(self, predecessors):
        if type(predecessors) != str:
            return predecessors
        predecessors = predecessors.split(",")

        return predecessors

    #For printer only
    def getDurationStr(self):
        if (type(self.duration) != list):
            return str(self.duration)
        return ",".join(self.duration)

    def getPredecessorsStr(self):
        if (type(self.predecessors) != list):
            return str(self.predecessors)
        return ",".join(self.predecessors)
    
    def getSuccessorsStr(self):
        if (type(self.successors) != list):
            return str(self.successors)
        return ",".join(self.successors)