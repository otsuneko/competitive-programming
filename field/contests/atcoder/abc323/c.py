import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def sort_with_index(arr, reverse=False):
    if reverse:
        return sorted([ (x,i) for i, x in enumerate(arr)], reverse=True)
    else:
        return sorted([ (x,i) for i, x in enumerate(arr)])

N,M = map(int,input().split())
A = list(map(int,input().split()))
S = [list(input()) for _ in range(N)]

score = [i+1 for i in range(N)]
for i in range(N):
    for j in range(M):
        if S[i][j] == "o":
            score[i] += A[j]

ma = max(score)
A = sort_with_index(A,reverse=True)

for i in range(N):
    cur = score[i]
    ans = 0
    for s,j in A:
        if cur >= ma:
            print(ans)
            break
        if S[i][j] == "x":
            cur += s
            ans += 1
    else:
        print(ans)
