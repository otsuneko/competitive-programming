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
crt = int(N**(0.5))
primes = sieve(crt)
M = len(primes)
# print(primes)

ans = 0
for i in range(M):
    a = primes[i]
    A = a**2
    if A > N:
        break
    for j in range(i+1,M):
        b = primes[j]
        if A * b > N:
            break
        for k in range(j+1,M):
            c = primes[k]
            if A * b * (c**2) > N:
                break
            ans += 1
    
print(ans)