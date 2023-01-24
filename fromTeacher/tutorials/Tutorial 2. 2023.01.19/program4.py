def SumOfValues(values):
    sum = 0
    i = 0
    while i<len(values):
        sum = sum + values[i]
        i = i + 1
    return sum
    
L = [1, 2, 3, 4, 100]
print(SumOfValues(L))

def SumOfValues2(values):
    sum = 0
    for value in values:
        sum = sum + value
    return sum

print(SumOfValues2(L))

def CreateListOfSumsOfValues(values):
    sumOfValues = []
    sum = 0
    for value in values:
        sum = sum + value
        sumOfValues.append(sum)
    return sumOfValues

S = CreateListOfSumsOfValues(L)
print(S)
