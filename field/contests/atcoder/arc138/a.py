from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
N,K =map(int,input().split())
A = list(map(int,input().split()))

li = []
ma = 0
for i in range(K,N):
    if A[i] <= ma:
        continue
    li.append((A[i],i))
    ma = max(ma,A[i])

li.sort(key=lambda x:(x[0],x[1]))

ans = 10**18
for i in range(K):
    idx = bisect(li,(A[i],10**9))
    if idx < len(li):
        ans = min(ans, li[idx][1]-i)

if ans == 10**18:
    print(-1)
else:
    print(ans)