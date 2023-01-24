# M = [[0, 0], [1, 7], [3, 20], [4, 15], [10, 30]]

def EmpiricalFunction_New():
    return []

def EmpiricalFunction_AddPoint(function, x, y):
    inserted = False
    i = 0
    while i<len(function):
        point = function[i]
        px = point[0]
        if px==x:
            point[1] = y
            inserted = True
            break
        if px>x:
            newPoint = [x, y]
            function.insert(i, newPoint)
            inserted = True
            break
        i = i + 1
    if not inserted:
        newPoint = [x, y]
        function.append(newPoint)

def InterpolateValue(point1, point2, x):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    y = y1 + ((y2-y1)/(x2-x1))*(x-x1)
    return y

def EmpiricalFunction_CalculateValue(function, x):
    if len(function)==0:
        return 0
    inserted = False
    i = 0
    while i<len(function):
        point = function[i]
        px = point[0]
        if px==x:
            y = point[1]
            return y
        if px>x:
            previousPoint = function[i-1]
            nextPoint = function[i]
            y = InterpolateValue(previousPoint, nextPoint, x)
            return y
        i = i + 1
    if not inserted:
        newPoint = [x, y]
        function.append(newPoint)

M = EmpiricalFunction_New()
EmpiricalFunction_AddPoint(M, 0, 0)
EmpiricalFunction_AddPoint(M, 1, 7)
EmpiricalFunction_AddPoint(M, 10, 30)
EmpiricalFunction_AddPoint(M, 3, 200)
EmpiricalFunction_AddPoint(M, 3, 20)

y = InterpolateValue([4,15], [10,30], 10)
print(y)



