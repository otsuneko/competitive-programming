from collections import Counter

def is_ok(arg):
    status2 = []
    for s in status:
        tmp = [0]*5
        for j in range(5):
            tmp[j] = 1 if s[j] >= arg else 0
        status2.append(tuple(tmp))
    count = Counter(status2)

    # print(arg, status2)

    for key1 in count:
        for key2 in count:
            for key3 in count:
                if count[key1] + count[key2] + count[key3] < 3:
                    continue
                mi = 10**18
                for i in range(5):
                    mi = min(mi, max(key1[i], key2[i], key3[i]))
                if mi == 1:
                    return True

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

status = []
ma = [0]*5
for i in range(N):
    s = list(map(int,input().split()))
    for i in range(5):
        ma[i] = max(ma[i], s[i])
    status.append(s)

ans = meguru_bisect(sum(ma),0)
print(ans)