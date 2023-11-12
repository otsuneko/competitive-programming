import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

cnt = [[] for _ in range(37)]
num = [0]*N

for i in range(N):
    C = int(input())
    num[i] = C
    A = list(map(int,input().split()))
    for a in A:
        cnt[a].append(i+1)
X = int(input())

li = []
for p in cnt[X]:
    li.append(num[p-1])

ans = []
if not li:
    print(0)
    print()
    exit()
mi = min(li)
for p in cnt[X]:
    if num[p-1] == mi:
        ans.append(p)
print(len(ans))
print(*ans)