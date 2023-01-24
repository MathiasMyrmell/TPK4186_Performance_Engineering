def factorial(n):
    result = 1
    step = 1
    while step<=n:
        result = result * step
        step = step + 1
    return result

n = 10
result = factorial(n)
print(str(n) + "! = " + str(result))

n = 15
result = factorial(n)
print(str(n) + "! = " + str(result))


