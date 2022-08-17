def is_ok(arg):
    if A+D*(arg-1) >= X:
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

def is_ok2(arg):
    if A+D*(arg-1) <= X:
        return True
    else:
        return False

def meguru_bisect2(ng, ok):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

X,A,D,N = map(int,input().split())

if A <= X <= A+D*(N-1):
    li = []
    n = meguru_bisect(0,N+1)
    for i in range(-5,5):
        if 0 <= n+i <= N-1:
            li.append(A+D*(n+i))
    # print(lower,upper)

    ans = min([abs(X-l) for l in li])
elif A+D*(N-1) <= X <= A:
    li = []
    n = meguru_bisect2(N+1,0)
    for i in range(-5,5):
        if 0 <= n+i <= N-1:
            li.append(A+D*(n+i))
    # print(lower,upper)

    ans = min([abs(X-l) for l in li])
else:
    ans = min(abs(X-A),abs(X-(A+D*(N-1))))
print(ans)
