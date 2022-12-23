def is_ok(arg):
    # 条件を満たすかどうか？問題ごとに定義
    
    time_limit = []
    for baloon in baloons:
        H,S = baloon
        if arg-H < 0:
            return False
        time_limit.append((arg-H)//S)
    time_limit.sort()

    now = 1
    for i in range(1,N):
        if time_limit[i] < now:
            return False
        now += 1
    
    return True

def meguru_bisect(ng, ok):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

N =int(input())
baloons =[list(map(int,input().split())) for _ in range(N)]

ans = meguru_bisect(-1,10**18)
print(ans)