N = int(input())

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

from collections import defaultdict
dict = defaultdict(int)
for ab in range(1,N):
    dict[ab] = len(divisor(ab))

ans = 0
for ab in range(1,N):
    cd = N-ab
    ans += dict[ab]*dict[cd]

print(ans)