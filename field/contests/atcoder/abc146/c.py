def is_ok(n,a,b,x):
    if a*n + b*(len(str(n))) <= x:
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
        if is_ok(mid,A,B,X):
            ok = mid
        else:
            ng = mid
    return ok

A,B,X = map(int,input().split())
print(meguru_bisect(10**9+1,0))