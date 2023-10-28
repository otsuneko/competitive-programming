import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

def dfs(i,j,k):
    if memo[i][j][k] >= 0:
        return memo[i][j][k]
    if [i,j,k] == [0,0,0]:
        return 0.0

    res = 0.0
    if i > 0:
        res += dfs(i-1,j,k)*i
    if j > 0:
        res += dfs(i+1,j-1,k)*j
    if k > 0:
        res += dfs(i,j+1,k-1)*k
    res += N
    res /= (i+j+k)

    memo[i][j][k] = res
    return res

N = int(input())
A = list(map(int,input().split()))

one = two = three = 0
for i in range(N):
    match A[i]:
        case 1:
            one += 1
        case 2:
            two += 1
        case 3:
            three += 1

memo = [[[-1]*(N+1) for _ in range(N+1)] for _ in range(N+1)]
print(dfs(one,two,three))
