import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
goods = []
for _ in range(N):
    s,t = map(int,input().split())
    goods.append((s,s+t))

# 昇順降順を入れ替える場合はlambda式の正負を反転
goods.sort(key=lambda x:(x[1],x[0]))
# print(goods)
now = 0
ans = 0

for s,t in goods:
    if now <= t:
        now = max(now+1,s+1)
        ans += 1
print(ans)