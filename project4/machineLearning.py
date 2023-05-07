import openpyxl
from task import Task
from pert import PERT
import random
import copy

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier,  KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

class ML():
    

    def __init__(self):
        self.standardProjects = {}
        self.projects = {}

    def loadFile(self, path):
        wb = openpyxl.load_workbook(path)
        ws = wb.active
        tasks = []
        for i in range(2, ws.max_row+1):
            id = i-1
            type = ws.cell(row=i, column=1).value
            if type == None :
                continue
            
            code = ws.cell(row=i, column=2).value
            description = ws.cell(row=i, column=3).value
            durations = ws.cell(row=i, column=4).value
            task = Task(id, type, code, description, durations)

            tasks.append(task)
        # Add predecessors and successors
        self._addPreAndSuc(tasks, wb) 
        projectName = path.split("/")[-1].split(".")[0]
        self.standardProjects[projectName] = tasks
        # return #tasks#self.projects.append(PERT(tasks))
    

    def _addPreAndSuc(self,tasks, wb):
        ws = wb.active
        # Add predecessors
        for i in range(2, ws.max_row+1):
            type = ws.cell(row=i, column=1).value
            if type == None :
                continue
            for task in tasks:
                code = ws.cell(row=i, column=2).value
                predecessors = []
                successors = []
                if task.code == code:
                    # print("Code: ", code)
                    # Add predecessors
                    predecessorsStr = ws.cell(row=i, column=5).value
                    if predecessorsStr == None:
                        continue
                    else:
                        predecessorsStr = predecessorsStr.replace(" ", "").split(",")
                    for pre in predecessorsStr:
                        for t in tasks:
                            if t.code == pre:
                                predecessors.append(t)
                    task.setPredecessors(predecessors)

        # Add successorts
        for t in tasks:
            # Find predeccsors to task
            for pre in t.predecessors:
                # for each predeccesor, add task as successor
                for task in tasks:
                    if task.code == pre.code:
                        task.successors.append(t)


    # #Preprocess data
    # Task 4
    def preprocessData(self):
        # Create 1000 projects per risk factor for each project
        for key, value in self.standardProjects.items():
            # print("Project: ", key)
            # print("Tasks: ", value)
            self._task4(key,value)

    def _task4(self, projectName, tasks):
        standardProjects = []
        # # Calculate new durations
        riskFactors = [0.8,1.0,1.2,1.4]
        tasksCopy = copy.deepcopy(tasks)
        for factor in riskFactors:
            # print("Risk factor: ", factor)
            for task in tasksCopy:
                duration = task.getDurations()
                # print("oldDuration",duration)
                newDuration = self._calculateNewDuration(duration, factor)
                # print("newDuration",newDuration)
                task.setDurations(newDuration)

            #Create Diagram

            diagram = PERT(projectName, tasks, factor)
            # diagram.printEarlyAndLateDates()
            # diagram.getDurations()
            standardProjects.append(diagram)

        # Standard time for project for each risk factor
        # expectedRunningTime = {}
        # for p in range(len(riskFactors)):
        #     demo = copy.deepcopy(standardProjects[p])
        #     finishTime = demo.executeProject().finishTime
        #     # print(finishTime)
        #     expectedRunningTime[riskFactors[p]] = finishTime

        # print("Expected running time: ", expectedRunningTime)

        # Create 1000 random projects per risk factor
        projects = {}
        for r in riskFactors:
            projects[r] = []
        # print(projects)
        for i in range(len(riskFactors)):
            base = standardProjects[i]
            # print("Risk factor: ", riskFactors[i])
            for j in range(0,5):##1000
                proj = copy.deepcopy(base)
                projNewDuration = self._randomDuration(proj)
                executed = projNewDuration.executeProject()
                # executed.getDuration()
                # print(executed.finishTime)
                # executed.printEarlyAndLateDates()
                projects[riskFactors[i]].append(executed)
                self.addProjectToDict(executed)

        # factor8 = projects[0.8]
        # for p in factor8:
        #     # print(p)
        #     p.getDurations()

        # Classify projects
        self._classifyProjects(projects)

    def _calculateNewDuration(self, duration, factor):
        newDuration = []
        if(type(duration) != list):
            return duration
        newExpected = round(duration[1]*factor,3)
        oldMinimum = duration[0]
        oldExpected = duration[1]
        oldMaximum = duration[2]
        if(newExpected<oldMinimum):
            newDuration = [newExpected, oldExpected, oldMaximum]
        elif(newExpected>oldMaximum):
            newDuration = [oldMinimum, oldExpected, newExpected]
        else:
            newDuration = [oldMinimum, newExpected, oldMaximum]
        return newDuration

    def _randomDuration(self, proj):
        project = copy.deepcopy(proj)
        tasks = project.tasks
        for task in tasks:
            if task.getDurations() == None:
                continue
            else:
                selectedDuration = random.choice(task.getDurations())
                task.setDuration(selectedDuration)
        return project

    def _classifyProjects(self, projects):
        classification = {"Successfull": [], "Acceptable": [], "Failed": []}
        for key, value in projects.items():
            for p in value:
                eFinishTime = p.expectedTime
                finishTime = p.finishTime
                factor = finishTime/eFinishTime
                if factor <1.05:
                    p.projectClass = "Successfull"
                    classification["Successfull"].append(p)
                elif factor <1.15:
                    p.projectClass = "Acceptable"
                    classification["Acceptable"].append(p)
                else:
                    p.projectClass = "Failed"
                    classification["Failed"].append(p)
        for key, value in classification.items():
            print(key, len(value))#, value)


    ## Machine learning
    # Add gate to project
    # Assumption: Every project shall have the same gate
    def addIntermediateGates(self, projectName, gate):
        for project in self.projects[projectName]:
            project.addIntermediateGate(gate)

    def addProjectToDict(self, project):
        if project.name in self.projects:
            self.projects[project.name].append(project)
        else:
            self.projects[project.name] = [project]
    
    ## Create dict with all project.
    ## For each project, sub project are divided in a 80/20 split for training and test data
    def createInstancesDataClassification(self):
        # Copy data
        data = copy.deepcopy(self.projects)
        # Get attibutes and values for each project
        # Keep factors divided inside project
        instances = {}
        for key, factors in data.items():
            if key not in instances:
                instances[key] = {} 
            for factor in factors:
                attributes = self._getAttributes(factor)
                valueClassification, valueRegression = self._getValues(factor)
                factor = factor.riskFactor
                if factor not in instances[key]:
                    instances[key][factor] = []
                instances[key][factor].append([attributes, valueClassification, valueRegression])

        ##Split into Learning data and Test data
        #Find size of test data
        size = 0
        sizes = []
        for key, value in instances.items():
            for factor, projects in value.items():
                size +=len(instances[key][factor])
                sizes.append(size)

        #Split learning and test data 80/20 split
        learningTestData = {}
        for key, value in instances.items():
            learningTestData[key] = {"LearningData": [], "TestData": []}
        for key, value in instances.items():
            for factor, projects in value.items():
                for factor in projects:
                    #Lengt of test data
                    learningSize = len(learningTestData[key]["LearningData"])

                    if learningSize < (size/2)*0.8 :
                        learningTestData[key]["LearningData"].append(factor)

                    else:
                        learningTestData[key]["TestData"].append(factor)

        return learningTestData
    ## Get attributes for project
    ## Assumption: intermediate gate is not in attributes
    def _getAttributes(self, project):
        intGate = project.getTaskByCode(project.intermediateGate)
        headers, rows = project.getRows()
        completion = rows[4]
        i = 0
        stack = []
        visited = []
        for suc in intGate.successors:
            stack.append(suc)
        
        while stack:
            node = stack.pop(0)
            if node in visited:
                continue
            for suc in node.successors:
                if suc not in visited:
                    stack.append(suc)
            
            # Gjør logikk
            visited.append(node)

        
        # Get late end for all tasks
        lateEndDates = []
        for task in visited:
            for i in range(len(headers)):
                if task.code == headers[i]:
                    lateEndDates.append(completion[i])
                    break

        return lateEndDates


    def _getValues(self, project):
        valueClassification = project.projectClass
        valueRegression = project.finishTime
        return valueClassification, valueRegression
        


    def classification(self, learningTestData):
        classification = {}
        models = {}
        # Create empty dictionaries for further use
        for project, value in learningTestData.items():
            classification[project] = [],[]
            models[project] = None
        ## Sort out data for each project
        for project, value in learningTestData.items():
            learningData = value["LearningData"]

            for data in learningData:
                classification[project][0].append(data[0])
                classification[project][1].append(data[1])

        ## Create every model
        # 1. Support vector machine
        # 2. K nearest neighbour KNeighborsClassifier
        # 3. Decision tree DecisionTreeClassifier
        models = {}
        for project, value in classification.items():
            # self.trainModels(value, project)
            models[project] = self.trainModelsC(value, project)
            # attributes = value[0]
            # values = value[1]
            # print(project)
            # clf = svm.SVC()
            # model = clf.fit(attributes, values)
            # models[project] = model
            # SVC()
        print("models", models)
        ## Test data on model
        testResult = {}
        for project, model in models.items():
            # print("project", project)
            # print("value", value)
            # print("ltD", learningTestData[project])
            res = self.testModels(model, learningTestData[project]["TestData"])
            testResult[project] = res

        print("testResult", testResult)
        return testResult
    def trainModelsC(self, value, project):
        trainingModels = {"SVM": svm.SVC(), "KNeighborsClassifier": KNeighborsClassifier(), "DecisionTreeClassifier": DecisionTreeClassifier()}
        attributes = value[0]
        values = value[1]
        trainedModels = {}
        for name, model in trainingModels.items():
            trainedModel = model.fit(attributes, values)
            trainedModels[name] = trainedModel
        print("t",trainedModels)
        return trainedModels
            
        

    def testModels(self, models, data):
        testRestult = {}
        for modelName, model in models.items():
            testRes = self._performTest(model, data)
            testRestult[modelName] = testRes
        return testRestult
        # for project, value in data.items():
        #     print("project", project)
        #     print("value", value)
        # for project, value in data.items():
        #     print("project", project)
        #     print("value", value)
        #     # print(value["TestData"])
        #     model = models[project]
        #     testData = value["TestData"]
        #     testRes = self._performTest(model, testData)
        #     testRestult[project] = testRes
        # return testRestult


    def _performTest(self, model, testData):
        # print("testData", testData)
        correct = 0
        wrong = 0
        for data in testData:
            # print(data)
            attributes = data[0]
            value = data[1]
            modelRes = model.predict([attributes])
            # print("modelRes", modelRes)
            if modelRes == value:
                correct +=1
            else:
                wrong +=1
        return [correct, wrong] 
    


    def regression(self, learningTestData):
        regression = {}
        models = {}
        # Create empty dictionaries for further use
        for project, value in learningTestData.items():
            regression[project] = [],[]
            models[project] = None
        ## Sort out data for each project
        for project, value in learningTestData.items():
            learningData = value["LearningData"]

            for data in learningData:
                regression[project][0].append(data[0])
                regression[project][1].append(data[2])
        print("regr", regression)
        ## Create every model
        # 1. Support vector machine
        # 2. K nearest neighbour KNeighborsRegressor
        # 3. Decision tree DecisionTreeRegressor
        models = {}
        for project, value in regression.items():
            # self.trainModels(value, project)
            models[project] = self.trainModelsR(value, project)
            # attributes = value[0]
            # values = value[1]
            # print(project)
            # clf = svm.SVC()
            # model = clf.fit(attributes, values)
            # models[project] = model
            # SVC()
        print("models", models)
        ## Test data on model
        testResult = {}
        for project, model in models.items():
            # print("project", project)
            # print("value", value)
            # print("ltD", learningTestData[project])
            res = self.testModelsR(model, learningTestData[project]["TestData"])
            testResult[project] = res

        print("testResult", testResult)
        return testResult

    def trainModelsR(self, value, project):
        trainingModels = {"SVM": svm.SVR(), "KNeighborsRegressor": KNeighborsRegressor(), "DecisionTreeRegressor": DecisionTreeRegressor()}
        attributes = value[0]
        values = value[1]
        trainedModels = {}
        for name, model in trainingModels.items():
            trainedModel = model.fit(attributes, values)
            trainedModels[name] = trainedModel
        print("t",trainedModels)
        return trainedModels


    def testModelsR(self, models, data):
        testRestult = {}
        for modelName, model in models.items():
            testRes = self._performTestR(model, data)
            testRestult[modelName] = testRes
        return testRestult
        # for project, value in data.items():
        #     print("project", project)
        #     print("value", value)
        # for project, value in data.items():
        #     print("project", project)
        #     print("value", value)
        #     # print(value["TestData"])
        #     model = models[project]
        #     testData = value["TestData"]
        #     testRes = self._performTest(model, testData)
        #     testRestult[project] = testRes
        # return testRestult


    def _performTestR(self, model, testData):
        # print("testData", testData)
        for data in testData:
            # print(data)
            attributes = data[0]
            value = data[2]
            modelRes = model.predict([attributes])[0]
            # print("modelRes", modelRes)
            ##Calculate loss 
            loss = abs(modelRes - value)
        return [modelRes, value, loss] 