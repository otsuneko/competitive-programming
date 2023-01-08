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

def is_ok(arg,q):
    if primes[arg]*q > N:
        return True
    else:
        return False


def meguru_bisect(ng, ok,q):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid,q):
            ok = mid
        else:
            ng = mid
    return ok

T = int(input())
primes = sieve(10**7)
for _ in range(T):
    N = int(input())

    for p in primes:
        if N%p != 0:
            continue

        N //= p
        if N%p == 0:
            q = N//p
            print(p,q)
            break
        else:
            q = p
            p = int(N**0.5)
            print(p,q)
            break
