import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
N,Q =  map(int,input().split())
cnt = [set() for _ in range(N)]

ans = N
for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        u,v = query[1:]
        u,v = u-1,v-1
        if len(cnt[u]) == 0:
            ans -= 1
        cnt[u].add(v)
        if len(cnt[v]) == 0:
            ans -= 1
        cnt[v].add(u)
        print(ans)
    elif query[0] == 2:
        v = query[1]
        v -= 1
        sub = cnt[v]
        if len(cnt[v]) != 0:
            ans += 1
        cnt[v] = set()
        for s in sub:
            cnt[s].remove(v)
            if len(cnt[s]) == 0:
                ans += 1
        print(ans)