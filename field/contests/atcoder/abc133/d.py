def is_ok(arg):
    ini = arg
    for i in range(N):
        ini = A[i]-ini
    if ini <= arg:
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

N = int(input())
A = list(map(int,input().split()))

ini = meguru_bisect(-1,A[0]+1)
Mt = [0]*N
for i in range(N):
    Mt[i] = ini*2
    ini = A[i]-ini
print(*Mt)