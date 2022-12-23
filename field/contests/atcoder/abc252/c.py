N = int(input())
S = [list(input()) for _ in range(N)]

li = [[] for _ in range(10)]
for i in range(N):
    for j in range(10):
        li[int(S[i][j])-1].append(j)

for i in range(10):
    li[i].sort()

ans = 10**18
for i in range(10):
    t = li[i][0]
    cnt = 0
    for j in range(1,len(li[i])):
        if li[i][j] == li[i][j-1]:
            cnt += 1
        else:
            t = max(t,li[i][j-1]+10*cnt)
            cnt = 0
    t = max(t,li[i][j]+10*cnt)
    ans = min(ans, t)

print(ans)