import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,T = map(int,input().split())
A = list(map(int,input().split()))

yoko = []
for i in range(N):
    s = set()
    for j in range(N):
        s.add(i*N+j+1)
    yoko.append(s)

tate = []
for i in range(N):
    s = set()
    for j in range(N):
        s.add(j*N+i+1)
    tate.append(s)

naname = []
s = set()
s2 = set()
for i in range(N):
    s.add(i*N+i+1)
    s2.add(i*N+N-i)
naname.append(s)
naname.append(s2)

def is_ok(arg):
    s = set()
    for a in A[:arg]:
        s.add(a)
    for t in tate:
        if t <= s:
            return True
    for y in yoko:
        if y <= s:
            return True
    for n in naname:
        if n <= s:
            return True
    return False

def meguru_bisect(ng, ok):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

ans = meguru_bisect(0,T+1)
if ans == T+1:
    print(-1)
else:
    print(ans)
