# M = [[0, 0], [1, 7], [3, 20], [4, 15], [10, 30]]

# 1. Points
# ---------

def Point_New(x, y):
    return [x, y]

def Point_GetX(point):
    return point[0]

def Point_GetY(point):
    return point[1]

def Point_SetX(point, x):
    point[0] = x

def Point_SetY(point, y):
    point[1] = y

# 2. Empirical Functions
# ----------------------

def EmpiricalFunction_New():
    return []

def EmpiricalFunction_GetNumberOfPoints(function):
    return len(function)

def EmpiricalFunction_GetNthPoint(function, index):
    return function[index]

def EmpiricalFunction_GetFirstPoint(function):
    return function[0]

def EmpiricalFunction_GetLastPoint(function):
    return function[-1]

def EmpiricalFunction_InsertPoint(function, point, index):
    return function.insert(index, point)

def EmpiricalFunction_AppendPoint(function, point):
    return function.append(point)

def EmpiricalFunction_AddPoint(function, x, y):
    inserted = False
    i = 0
    while i<EmpiricalFunction_GetNumberOfPoints(function):
        point = EmpiricalFunction_GetNthPoint(function, i)
        px = Point_GetX(point)
        if px==x:
            Point_SetY(point, y)
            inserted = True
            break
        if px>x:
            newPoint = Point_New(x, y)
            EmpiricalFunction_InsertPoint(function, newPoint, i)
            inserted = True
            break
        i = i + 1
    if not inserted:
        newPoint = Point_New(x, y)
        EmpiricalFunction_AppendPoint(function, newPoint)

def EmpiricalFunction_InterpolateValue(point1, point2, x):
    x1 = Point_GetX(point1)
    y1 = Point_GetY(point1)
    x2 = Point_GetX(point2)
    y2 = Point_GetY(point2)
    y = y1 + ((y2-y1)/(x2-x1))*(x-x1)
    return y

def EmpiricalFunction_CalculateValue(function, x):
    if EmpiricalFunction_GetNumberOfPoints(function)==0:
        return 0
    if EmpiricalFunction_GetNumberOfPoints(function)==1:
        firstPoint = EmpiricalFunction_GetFirstPoint(function)
        return Point_GetY(firstPoint)
    firstPoint = EmpiricalFunction_GetFirstPoint(function)
    px = Point_GetX(firstPoint)
    if px>=x:
        return Point_GetY(firstPoint)
    lastPoint = EmpiricalFunction_GetLastPoint(function)
    px = Point_GetX(lastPoint)
    if px<=x:
        return Point_GetY(lastPoint)
    i = 1
    while i<EmpiricalFunction_GetNumberOfPoints(function):
        nextPoint = EmpiricalFunction_GetNthPoint(function, i)
        px = Point_GetX(nextPoint)
        if px==x:
            return Point_GetY(nextPoint)
        if px>x:
            previousPoint = EmpiricalFunction_GetNthPoint(function, i-1)
            return EmpiricalFunction_InterpolateValue(previousPoint, nextPoint, x)
        i = i + 1

def EmpiricalFunction_GetMinimum(function):
    if EmpiricalFunction_GetNumberOfPoints(function)==0:
        return 0
    firstPoint = EmpiricalFunction_GetFirstPoint(function)
    minimum = Point_GetY(firstPoint)
    i = 1
    while i<EmpiricalFunction_GetNumberOfPoints(function):
        point = EmpiricalFunction_GetNthPoint(function, i)
        y = Point_GetY(point)
        if y<minimum:
            minimum = y
        i = i + 1
    return minimum

def EmpiricalFunction_GetMaximum(function):
    if EmpiricalFunction_GetNumberOfPoints(function)==0:
        return 0
    firstPoint = EmpiricalFunction_GetFirstPoint(function)
    maximum = Point_GetY(firstPoint)
    i = 1
    while i<EmpiricalFunction_GetNumberOfPoints(function):
        point = EmpiricalFunction_GetNthPoint(function, i)
        y = Point_GetY(point)
        if y>maximum:
            maximum = y
        i = i + 1
    return maximum

def EmpiricalFuntion_CalculateIntegral(function, x1, x2):
    # To be completed
    pass

# 3. Printer
# ----------

def Printer_PrintPoint(point):
    x = Point_GetX(point)
    y = Point_GetY(point)
    print("(" + str(x) + ", " + str(y) + ")")
    
def Printer_PrintEmpiricalFunction(function):
    i = 0
    while i<EmpiricalFunction_GetNumberOfPoints(function):
        point = EmpiricalFunction_GetNthPoint(function, i)
        Printer_PrintPoint(point)
        i = i + 1


# 4. Main
# -------

M = EmpiricalFunction_New()
EmpiricalFunction_AddPoint(M, 0, 0)
EmpiricalFunction_AddPoint(M, 1, 7)
EmpiricalFunction_AddPoint(M, 10, 30)
EmpiricalFunction_AddPoint(M, 3, 200)
EmpiricalFunction_AddPoint(M, 3, 40)

Printer_PrintEmpiricalFunction(M)

y = EmpiricalFunction_CalculateValue(M, 0.5)
print(y)

print(EmpiricalFunction_GetMinimum(M))
print(EmpiricalFunction_GetMaximum(M))



