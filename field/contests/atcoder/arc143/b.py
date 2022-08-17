mod = 998244353

def fact(n):
    fact = [0 for _ in range(n + 1)]
    fact[0] = 1
    for i in range(1, n + 1):
        fact[i] = i * fact[i - 1] % mod
 
    return fact[n]

def nPr(n, k):
    if n < k:
        return 1

    fact = [0 for _ in range(n + 1)]
    fact[0] = 1
    for i in range(1, n + 1):
        fact[i] = i * fact[i - 1] % mod
 
    return fact[n] // fact[n - k]

N = int(input())

total = fact(N**2)
total = (total - N**2 * nPr(N**2,2*N-1) * fact((N-1)**2))%mod

print(total)