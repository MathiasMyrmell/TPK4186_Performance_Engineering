def CreateListOfSquares(maximumValue):
    L = []
    i = 1
    while i<=maximumValue:
        L.append(i*i)
        i = i + 1
    return L

L = CreateListOfSquares(20)
print(L)