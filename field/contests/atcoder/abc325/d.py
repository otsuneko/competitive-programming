import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
def debug(*args): print(*args, file=sys.stderr)

from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport

N = int(input())
goods = []
for _ in range(N):
    s,t = map(int,input().split())
    goods.append((s,s+t))
goods.sort()

ans = 0
idx = 0
cur = 0
hq = []
while idx < N or hq:
    # 印字可能な商品が無い区間はスキップ
    if idx < N and len(hq) == 0:
        cur = goods[idx][0]
    # 今印字可能になった商品を終了時刻が早い順にリストアップ
    while idx < N and goods[idx][0] == cur:
        heappush(hq,goods[idx][1])
        idx += 1
    # 終了時刻が現在時刻よりも早い商品を除外
    while hq and hq[0] < cur:
        heappop(hq)
    # 印字
    if hq:
        heappop(hq)
        ans += 1
        cur += 1

print(ans)