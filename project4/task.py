# # Task 1

class Task:

    def __init__(self, id, type, code, description, durations, predecessors = None):
        self.id = id
        self.type = type
        self.code = code
        self.description = description
        self.durations = self._durations(durations)
        self.predecessors = self._predecessors(predecessors)
        self.successors = []
        self.criticality = False

        self.duration = self._duration()
    ###Getters
    def getDurations(self):
        return self.durations
    
    def getPredecessors(self):
        return self.predecessors
    
    def getSuccessors(self):
        return self.successors
    
    def getType(self):
        return self.type

    def getCode(self):
        return self.code
    
    def getDuration(self):
        if self.duration == None:
            return None
        return self.duration



    ###Setters
    def setDurations(self, durations):
        self.durations = durations
    
    def setDuration(self, duration):
        self.duration = duration
    
    def setPredecessors(self, predecessors):
        self.predecessors = predecessors
    


    ###Functions
    ## In initialization
    def _duration(self):
        if type(self.durations) != list:
            return None
        return self.durations[1]
    
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
        if predecessors == None:
            return []
        elif type(predecessors) != str:
            return predecessors
        predecessors = predecessors.split(",")

        return predecessors
   
    # Return True if task is the start task in the project, else False
    def isStartTask(self):
        if len(self.predecessors) == 0:
            return True
        return False
    
    # Return True if task is the end task in the project, else False
    def isEndTask(self):
        if len(self.successors) == 0:
            return True
        return False


    ### For printing
    def getDescriptionStr(self):
        if (self.description == None):
            return ""
        return self.description
    
    def getDurationStr(self):
        if (type(self.durations) != list):
            return ""
        durationString = "("
        for d in range(len(self.durations)):
            durationString+=str(self.durations[d])
            if d != len(self.durations)-1:
                durationString+=","
        durationString+=")"
        return durationString

    def getPredecessorsStr(self):
        if (type(self.predecessors) != list):
            return ""
        predecessorsString = ""
        if len(self.predecessors) == 1:
            return self.predecessors[0].code
        else:
            for p in range(len(self.predecessors)):
                predecessorsString += str(self.predecessors[p].code)
                if p != len(self.predecessors)-1:
                    predecessorsString+=","
        return predecessorsString
    
    def getSuccessorsStr(self):
        if (type(self.successors) != list):
            return ""
        successorsString = ""
        if len(self.successors) == 1:
            return self.successors[0].code
        for s in range(len(self.successors)):
            successorsString += str(self.successors[s].code)
            if s != len(self.successors)-1:
                successorsString+=","
        return successorsString
    
    
    ### Representation
    def __str__(self):
        return self.code
    
    def __repr__(self):
        return self.__str__()

