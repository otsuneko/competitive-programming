N = int(input())
A = list(map(int,input().split()))

diff = min_diff = A.count(1)
idx = 0
for i in range(N):
    if A[i] == 1:
        diff -= 1
    else:
        diff += 1
    if diff < min_diff:
        min_diff = diff
        idx = i+1

ans = A[:idx].count(0) + A[idx:].count(1)
print(ans)