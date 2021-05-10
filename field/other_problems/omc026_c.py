def divisor(n):
    lower_divisors , upper_divisors = [], []
    i = 1
    while i*i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n//i)
        i += 1
    return lower_divisors + upper_divisors[::-1]

for i in range(1,10000):
    equation = i**4 + 24*(i**3)
    table = divisor(equation)
    if len(table) == 21:
        print(i)