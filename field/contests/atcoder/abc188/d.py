from collections import defaultdict
N,C = map(int,input().split())
d = defaultdict(int)

for _ in range(N):
    a,b,c = map(int,input().split())
    d[a] += c
    d[b+1] -= c

d = sorted(d.items(), key=lambda x:x[0])

ans = 0
cost = d[0][1]
now = d[0][0]
for k,v in d[1:]:
    ans += min(cost,C) * (k-now)
    cost += v
    now = k

print(ans)