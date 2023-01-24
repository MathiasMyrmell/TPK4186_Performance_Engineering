def factorial(n):
    if n==1:
        return 1
    return n * factorial(n - 1)

def binomial(n, p):
    if p==0 or p==n:
        return 1
    return binomial(n-1, p-1) + binomial(n-1, p)


n = 60
p = 6
result = binomial(n, p)

print("binomial(" + str(n) + ", " + str(p) + ") = " + str(result))


