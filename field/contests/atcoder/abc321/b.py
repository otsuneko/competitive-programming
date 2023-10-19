import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,X = map(int,input().split())
A = list(map(int,input().split()))

A.sort()
mi = A[0]
ma = A[-1]

def is_ok(arg):
    A2 = A[:]
    A2.append(arg)
    A2.sort()
    su = sum(A2) - A2[0] - A2[-1]

    if su >= X:
        return True
    else:
        return False

def meguru_bisect(ng, ok):
    '''
    初期値のng,okを受け取り,is_okを満たす最小(最大)のokを返す
    まずis_okを定義すべし
    ng ok は  とり得る最小の値-1 とり得る最大の値+1
    最大最小が逆の場合はよしなにひっくり返す
    '''
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

ans = meguru_bisect(-1,10**9)
if ans == 10**9:
    print(-1)
else:
    print(ans)