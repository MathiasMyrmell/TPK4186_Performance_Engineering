def factorial(n):
    result = 1
    step = 1
    while step<=n:
        result = result * step
        step = step + 1
    return result

def binomial(n, p):
    fn = factorial(n)
    fp = factorial(p)
    fnp = factorial(n - p)
    return fn // (fp * fnp)


n = 4
p = 2
result = binomial(n, p)

print("binomial(" + str(n) + ", " + str(p) + ") = " + str(result))


