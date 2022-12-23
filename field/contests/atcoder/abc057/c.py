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

N =int(input())
div = divisor(N)

ans = 10**18
for d in div:
    d2 = N//d
    ans = min(ans, max(len(str(d)),len(str(d2))))
print(ans)