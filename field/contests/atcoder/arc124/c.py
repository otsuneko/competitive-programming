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

N = int(input())
a,b = map(int,input().split())
red = divisor(a)
blue = divisor(b)

A = []
B = []
for _ in range(N-1):
    a,b = map(int,input().split())
    A.append(a)
    B.append(b)

ans = 0
for n_r in red:
    for n_b in blue:
        for i in range(N-1):
            if (A[i]%n_r or B[i]%n_b) and (B[i]%n_r or A[i]%n_b):
                break
        else:
            ans = max(ans, n_r*n_b)
            print(ans, n_r*n_b)

print(ans)
