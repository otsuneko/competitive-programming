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

K = int(input())
div = divisor(K)
check = set(div)

ans = 0
l = len(div)

for i in range(l):
    for j in range(i,l):
        k = K/div[i]/div[j]
        if k == int(k) and div[j] <= k and k in check:
            ans += 1
print(ans)