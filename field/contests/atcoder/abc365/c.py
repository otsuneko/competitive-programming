import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def is_ok(arg):

    su = sum(min(arg,A[i]) for i in range(N))
    if su <= M:
        return False
    else:
        return True

def meguru_bisect(ng, ok):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

N,M = map(int,input().split())
A = list(map(int,input().split()))

ans = meguru_bisect(-1,10**18)

if ans == 10**18:
    print("infinite")
else:
    print(ans-1)
