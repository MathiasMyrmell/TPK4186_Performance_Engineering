import copy
from prettytable import PrettyTable
class PERT:

    def __init__(self, tasks):
        self.tasks = tasks


    # def printer(self):
    #     print("PERT Diagram")
    #     print("Type\tDuration\tPredecessors\tSuccessors")
    #     for task in self.tasks:
    #         code = task.code
    #         duration = task.getDurationStr()
    #         predecessors = task.getPredecessorsStr()
    #         successors = task.getSuccessorsStr()
    #         print(f"{code}\t{duration}\t\t{predecessors}\t\t{successors}")
    def getFirstTask(self):
        for task in self.tasks:
            if task.predecessors == None:
                return task
        return None
    
    def getEndTask(self):
        return self.tasks[-1]

    def getTaskBycode(self, code):
        for task in self.tasks:
            if task.code == code:
                return task
        return None

    def printer(self):
        tasksCopy = copy.copy(self.tasks)
        # Calculate late completiondate 
        # print(len(self.tasks[0].predecessors))
        finishTime = self._finishTime(tasksCopy)
        print("finishTime",finishTime)
        lcd = self._getLateCompletionDate(tasksCopy, finishTime) 
        # print(taskCodes)
        # print(duration)

    # def _lateCompletionDate(self, tasks):
    #     firstTask = self.getFirstTask()
    #     for successor in firstTask.successors:

    def _finishTime(self, tasks):
        endGate = self.getEndTask()
        earlyDate = []
        for task in endGate.predecessors:
            # print("pre", task.code)
            earlyDate.append(self.getFinishTime(task))
        return earlyDate[0]


    def getFinishTime(self, task):
        # print("task",task)
        earlyDate = []
        # earlyDate = {}
        if len(task.predecessors) == 0:
            return 0
            # return {task.code: 0}
        else:
            for predecessor in task.predecessors:
                earlyDate.append(self.getFinishTime(predecessor))
            return max(earlyDate) + task.duration[1]
            # for predecessor in task.predecessors:
            #     p = self.getFinishTime(predecessor)
            #     for key in p:
            #         earlyDate[key] = p[key]
            #     earlyDate[task.code] = task.getDuration()
        # return earlyDate      

    def _getLateCompletionDate(self, tasksCopy, finishTime):
        duration = []
        taskCodes = []
        # Get task codes and durations
        for task in tasksCopy:
            taskCodes.append(task.code)
            if task.duration == None:
                duration.append(0)
            else:
                duration.append(task.duration[1])

        earlyStartDate = [0]*len(taskCodes)
        earlyCompletionDate = [0]*len(taskCodes)
        lateStartDate = [0]*len(taskCodes)
        lateCompletionDate = [0]*len(taskCodes)
        

        #Add finihtimes
        earlyStartDate[-1] = finishTime
        earlyCompletionDate[-1] = finishTime
        lateStartDate[-1] = finishTime
        lateCompletionDate[-1] = finishTime



       
        # Calculate Late start and completion date
        for i in reversed(range(1,len(taskCodes)-1)):
            #TaskCode
            taskCode = taskCodes[i]
            # Task
            task = self.getTaskBycode(taskCode)
            # Duration of task
            taskDuration = task.getDuration()
            

            # successor of task
            successors = task.successors
            latestCompletionDate = float("inf")
            # print("------------------")
            # print("taskCode",taskCode)
            # print("successors",successors)
            for suc in successors:
                # Successor index
                sucIndex = taskCodes.index(suc.code)
                #Late start date of successor
                lateStartDateSuc = lateStartDate[sucIndex]
                #Late completion date of task
                # print("lateStartDateSuc",lateStartDateSuc)
                if lateStartDateSuc < latestCompletionDate:
                    latestCompletionDate = lateStartDateSuc
            # print("latestCompletionDate",latestCompletionDate)
            #Late start date of task
            lateStartDateTask = latestCompletionDate - taskDuration
            #Late completion date of task
            lateCompletionDate[i] = latestCompletionDate
            #Late start date of task
            lateStartDate[i] = latestCompletionDate - taskDuration


            # Predecessors to Task
            predecessors = self.getTaskBycode(taskCode).predecessors
            if(taskCode == "A"):
                break
        for i in range(1,len(taskCodes)-1):
            taskCode = taskCodes[i]
            #predecessors
            predecessors = self.getTaskBycode(taskCode).predecessors
            # print("------------------")
            # print("taskCode",taskCode)
            est = 0
            for pre in predecessors:
                # print("pre",pre.code)
                # Predecessor index
            
                preIndex = taskCodes.index(pre.code)
                # print("preIndex",preIndex)
                if est < earlyCompletionDate[preIndex]:
                    est = earlyCompletionDate[preIndex]
                # print("earlyStartDate",est)
            #Early completion date
            ecd = est + duration[i]
            earlyStartDate[i] = est
            earlyCompletionDate[i] = ecd

        table = PrettyTable()
        # table.field_names = [taskCodes[0], taskCodes[1], taskCodes[2], taskCodes[3], taskCodes[4], taskCodes[5], taskCodes[6], taskCodes[7], taskCodes[8], taskCodes[9], taskCodes[10], taskCodes[11]]
        table.add_row(duration)
        table.add_row(earlyStartDate)
        table.add_row(earlyCompletionDate)
        table.add_row(lateStartDate)
        table.add_row(lateCompletionDate)
        print(table)

        print("taskCodes","\t\t",taskCodes)
        print("Duration","\t\t",duration)
        print("earlyStartDate","\t\t",earlyStartDate)
        print("earlyCompletionDate","\t",earlyCompletionDate)
        print("lateStartDate","\t\t",lateStartDate)
        print("lateCompletionDate","\t",lateCompletionDate)


    # def _getLateCompletionDate(self, tasksCopy, finishTime):
    #     lcd = {} # key = [Late Start date, Late Completion date]
    #     # Add last task to dict
    #     endTask = self.getEndTask().predecessors[0]
    #     lcd[endTask.code] = [finishTime-endTask.getDuration(), finishTime]
    #     print("lcd",lcd)
    #     for predecessor in endTask.predecessors:
    #         # print("------------------")
    #         # print("predecessor",predecessor.code)
    #         # print("endtime", lcd[endTask.code][0])
    #         # print("duration", predecessor.getDuration())
    #         lcd[predecessor.code] = [lcd[endTask.code][0]-predecessor.getDuration(), lcd[endTask.code][0]]
    #         liste = self.getLateDate(predecessor, lcd)
    #         for key in liste:
    #             lcd[key] = liste[key]
    #     print("lcd",lcd)
        

    # def getLateDate(self,predecessor, lcd):
    #     lateDate = {}
    #     print("------------------")
    #     print("predecessor",predecessor.code)
    #     for pre in predecessor.predecessors:
    #         lateDate[pre.code] = [0,0]
    #         for p in pre.predecessors:
    #             liste = self.getLateDate(p, lcd)
    #             for key in liste:
    #                 lcd[key] = liste[key]
    #     return lateDate




    