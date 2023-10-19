import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = [list(input()) for _ in range(N)]

win = [0]*N
for i in range(N):
    for j in range(N):
        if S[i][j] == "o":
            win[i] += 1

def sort_with_index(arr, reverse=False):
    if reverse:
        return sorted([ (x,i) for i, x in enumerate(arr)], reverse=True)
    else:
        return sorted([ (x,i) for i, x in enumerate(arr)])

res = sort_with_index(win,reverse=True)
res.sort(key=lambda x:(-x[0],x[1]))
ans = []
for x,i in res:
    ans.append(i+1)
print(*ans)