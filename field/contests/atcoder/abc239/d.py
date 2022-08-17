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

A,B,C,D =map(int,input().split())

primes = set(sieve(300))

for takahashi in range(A,B+1):
    cnt = 0
    for aoki in range(C,D+1):
        if (takahashi + aoki) in primes:
            cnt += 1
    if cnt == 0:
        print("Takahashi")
        exit()

print("Aoki")