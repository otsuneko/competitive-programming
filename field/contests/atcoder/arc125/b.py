import bisect

def is_ok(mid,s):
    if mid**2 - s > 0:
        return True
    else:
        return False


def meguru_bisect(ng, ok,s):

    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid,s):
            ok = mid
        else:
            ng = mid
    return ok

N = int(input())
mod = 998244353

sq = []
k = 0
while k**2 < 10**12:
    sq.append(k**2)
    k += 1

ans = 0
idx = bisect.bisect(sq,N)
for s in sq[:N]:

    id = meguru_bisect(1,N+1,s)
    ans = (ans+N-id)%mod

print(ans)