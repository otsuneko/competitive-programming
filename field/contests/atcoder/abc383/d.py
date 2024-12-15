import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def sieve(n):
    is_prime = [True for _ in range(n+1)]
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, n+1):
        if not is_prime[i]:
            continue
        for j in range(i*2, n+1, i):
            is_prime[j] = False
    table = [ i-1 for i in range(1, n+1) if is_prime[i-1]] # 素数のリスト
    return table

N = int(input())
primes = sieve(10**7+1)

ans = set()
# n**8パターン
idx = 0
p = primes[idx]
while p**8 <= N:
    ans.add(p**8)
    idx += 1
    p = primes[idx]

# n**2 * m**2パターン
for p in primes:
    idx = 0
    q = primes[idx]
    while p**2 * q**2 <= N:
        if p != q:
            ans.add(p**2 * q**2)
        idx += 1
        q = primes[idx]

print(len(ans))
