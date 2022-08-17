N,Q =map(int,input().split())

manhattan = []
chebyshev = []
ma,mi = [-10**18,-10**18], [10**18,10**18]
for _ in range(N):
    x,y =map(int,input().split())
    manhattan.append((x,y))
    chebyshev.append((x-y,x+y))
    ma = [max(ma[0], x-y), max(ma[1], x+y)]
    mi = [min(mi[0], x-y), min(mi[1], x+y)]

for _ in range(Q):
    q =int(input())-1

    ans = 0
    for dim in range(2):
        ans = max(ans, ma[dim]-chebyshev[q][dim], chebyshev[q][dim]-mi[dim])

    print(ans)