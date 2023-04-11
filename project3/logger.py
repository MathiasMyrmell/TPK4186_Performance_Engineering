
import datetime
import sys
class Logger:
    def __init__(self, path):
        self.log = {}
        self.path = path+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace(" ","_").replace("/",".")+".txt"

    # # Getters
    # Returns log
    def getLog(self):
        return self.log

    def logEvent(self, time, event):
        if time in self.log:
            self.log[time].append(event)
        else:
            self.log[time] = [event]

    # # Functions
    # Saves log to file
    def saveToFile(self, info):
        
        #Create new file
        self._createFile()

        # Create header
        self._createHeader(info)

        # Write to file
        self._writeEventsToFile()

    # Creates file for this logger
    def _createFile(self):
        path = self.path
        try:
            f = open(path, "x")
            f.close()
        except:
            print("could not create file")
        return 0
    
    # Creates header for file
    def _createHeader(self, info):
        try:
            file = open(self.path, "r")
            file.close()
        except:
            print("could not read file")
        # try:
        file = open(self.path, "a")
        file.write("Metadata\n----------------------------------------\n")
        file.write("Productions goal: "+str(info[0])+"\n")
        #Tasks
        for i in range(0, len(info[1])):
            unitNr = i+1
            file.write("Unit "+str(unitNr)+"\n")
            for task in info[1][i]:
                file.write("\t"+"Task "+str(task)+"\n")
            file.write("Heuristics: "+str(info[2][i])+"\n")
        file.write("Time between loading to inputbuffer: "+ str(info[3])+"\n")
        file.write("Grouping of batches: "+ str(info[4])+"\n")
        file.write("----------------------------------------\n")
        file.flush()
        file.close()
        # except:
        #     print("could not append to file")
        return 0

    # Writes to file
    def _writeEventsToFile(self):
        try:
            file = open(self.path, "r")
            file.close()
        except:
            print("could not read file")
        try:
            file = open(self.path, "a")
            file.write("\nSimulation log\n----------------------------------------\n")
            times = self.log.keys()
            for time in times:
                newTime = True
                for event in self.log[time]:
                    if newTime == True:
                        file.write("\n{0:f}\t{1:s}".format(time, event))
                        newTime = False
                    else:
                        file.write("\n{0:s}\t{1:s}".format("\t", event))
                newTime = True

            file.flush()
            file.close()
        except:
            print("could not append to file")
        # sys.stdout.write("Simulation log saved to file: "+self.path+"\n")
        return 0
    