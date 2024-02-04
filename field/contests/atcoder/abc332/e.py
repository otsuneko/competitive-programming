import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

N,D = map(int,input().split())
W = list(map(int,input().split()))
W.sort(reverse=True)
ans = INF
mean = sum(W)/D

def dfs(cur,weight):
    if cur == N:
        variance = 0
        for w in weight:
            variance += (w-mean)**2
        variance /= D
        ans = min(ans,variance)
        return
    
    ma = weight[0]
    for i in range(D):
        if weight[i] == 0:
            weight[i] += W[cur]
            dfs(cur+1,weight)
    
    for 