def Fibonacci(n):
    if n<=1:
        return 1
    return Fibonacci(n-1) + Fibonacci(n-2)

def FastFibonacci(n):
    if n<=1:
        return 1
    Fn_2 = 1
    Fn_1 = 1
    i = 2
    while i<=n:
        Fn = Fn_1 + Fn_2
        Fn_2 = Fn_1
        Fn_1 = Fn
        i = i + 1
    return Fn
    
print(FastFibonacci(100))

def CreateListOfFibonacciNumbers(maximumValue):
    L = []
    i = 0
    while i<=maximumValue:
        L.append(FastFibonacci(i))
        i = i + 1
    return L

Fs = CreateListOfFibonacciNumbers(1000)
print(Fs)

def FastCreateListOfFibonacciNumbers(maximumValue):
    if maximumValue==0:
        return [1]
    if maximumValue==1:
        return [1, 1]
    L = [1, 1]
    Fn_2 = 1
    Fn_1 = 1
    i = 2
    while i<=maximumValue:
        Fn = Fn_1 + Fn_2
        Fn_2 = Fn_1
        Fn_1 = Fn
        L.append(Fn)
        i = i + 1
    return L

Fs = FastCreateListOfFibonacciNumbers(1000)
print(Fs)
