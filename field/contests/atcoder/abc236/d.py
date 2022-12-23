# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)

def dfs(check,score):
    global ans

    if len(check) == 2*N:
        ans = max(ans,score)
        return

    p1 = min(list(member - check))
    check.add(p1)

    for p2 in range(2*N):
        if p2 not in check:
            check.add(p2)
            if p1 < p2:
                dfs(check,score^A[p1][p2])
            else:
                dfs(check,score^A[p2][p1])
            check.remove(p2)
    
    check.remove(p1)

N =int(input())
member = set([i for i in range(2*N)])

A = [[0] * 2*N for _ in range(2*N)]
for i in range(2*N-1):
    tmp =list(map(int,input().split()))
    A[i][i+1:] = tmp

ans = 0
check = set()
dfs(check,0)
print(ans)