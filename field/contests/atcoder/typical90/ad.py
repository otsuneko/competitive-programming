def sieve(n):
    ret = [0]*(n+1)
    is_prime = [True for _ in range(n+1)]
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, n+1):
        if not is_prime[i]:
            continue
        for j in range(i*2, n+1, i):
            is_prime[j] = False
            ret[j] += 1

    return ret

N,K =map(int,input().split())
li = sieve(N)

ans = 0
for i in li:
    if i >= K:
        ans += 1
if K == 1:
    ans = N-1
print(ans)