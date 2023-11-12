import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

def dfs(s,bit):

    bits[s] = bit
    bit = (bit+1)%2
    for to in graph[s]:
        if bits[to] == -1:
            dfs(to,bit)
        else:
            if bits[to] != bit:
                print("No")
                exit()

N,M = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

graph = [[] for _ in range(N)]
for i in range(M):
    a,b = A[i],B[i]
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

bits = [-1]*N

for i in range(N):
    if bits[i] == -1:
        dfs(i,0)
# print(bits)
print("Yes")