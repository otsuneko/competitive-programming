from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
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

def is_ok(p,q):
    if p*(q**3) <= N:
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

N =int(input())
primes = sieve(10**7)

ans = 0
for q in primes[1:]:
    if q**3 > N:
        break
    p = meguru_bisect(q,1,q)
    # print(p,q)
    idx = bisect(primes,p)
    # print(idx)
    ans += idx

print(ans)