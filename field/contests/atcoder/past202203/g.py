def f(x):
    return a*x**5 + b*x + c

def meguru_bisect(ng, ok):
    while (abs(ok - ng) > delta):
        mid = (ok + ng) / 2
        if f(mid) > 0:
            ok = mid
        else:
            ng = mid
    return ok

a,b,c =map(int,input().split())
delta = 10**-12
print(meguru_bisect(1,2))