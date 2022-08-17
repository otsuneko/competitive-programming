def is_ok(arg):
    global ans
    X = (a+arg)*(a**2+arg**2)

    if X >= N:
        ans = min(ans,X)
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

N =int(input())
ans = 10**18
for a in range(10**6+1):
    meguru_bisect(-1,10**6+1)
    
print(ans)
