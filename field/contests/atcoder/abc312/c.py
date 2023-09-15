import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

def is_ok(arg):
    if bisect(A,arg) >= M - bisect_left(B,arg):
        return True
    else:
        return False

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
B = list(map(int,input().split()))

A.sort()
B.sort()

# print(A)
# print(B)

ans = meguru_bisect(-1,10**18)

sell = bisect(A,ans)
buy = M-bisect_left(B,ans)
# print(ans,sell,buy)
if sell >= buy:
    print(ans)
else:
    print(B[buy]+1)