
import datetime

class Logger:
    def __init__(self, simulator):
        self.simulator = simulator
        self.log = []
        self.path = "project3/files/"+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace(" ","_").replace("/",".")+".txt"

    # Logs event
    def logEvent(self, event):
        time = self.simulator.getTime()
        self.log.append([time, event])

    # Saves log to file
    def saveToFile(self):
        
        #Create new file
        self._createFile()

        # Create header
        self._createHeader()

        # Write to file
        self._writeToFile()

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
    def _createHeader(self):
        pass

    # Writes to file
    def _writeToFile(self):
        try:
            file = open(self.path, "r")
            file.close()
        except:
            print("could not read file")
        try:
            file = open(self.path, "a")
            for event in self.log:
                file.write(str(event[0]) + ": " + event[1])
                file.write("\n")
            file.flush()
            file.close()
        except:
            print("could not append to file")
        return 0