import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
ice =  [list(map(int,input().split())) for _ in range(N)]

from collections import defaultdict
dict = defaultdict(int)
ans = 0
for i in range(N):
    f,s = ice[i]
    if dict[f] > 0:
        ans = max(ans, max(dict[f],s) + min(dict[f],s)//2)
    dict[f] = max(dict[f], s)

# print(dict)

li = []
for key in dict:
    li.append(dict[key])

li.sort(reverse=True)

if len(li) >= 2:
    ans = max(ans, li[0]+li[1])

print(ans)