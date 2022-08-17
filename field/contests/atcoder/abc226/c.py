# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)
def dfs(s):

    if s in check:
        return 0
    check.add(s)

    t = time[s]

    for to in G[s]:
        t += dfs(to)
    
    return t

N = int(input())
time = [0]*N
G = [[] for _ in range(N)]
check = set()
for i in range(N):
    inp = list(map(int,input().split()))
    time[i] = inp[0]
    K = inp[1]
    A = inp[2:]
    for a in A: 
        G[i].append(a-1)

ans = dfs(N-1)
print(ans)