from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N = int(input())
A = list(map(int,input().split()))
A.sort()

idx = bisect(A,A[N-1]//2)

mi = 10**18
midx = 0
for i in range(idx-3,idx+3):
    if not (0<=i<N-1):
        continue
    if abs(A[N-1]//2-A[i]) <= mi:
        mi = abs(A[N-1]//2-A[i])
        midx = i


if midx == N-1:
    midx -= 1

print(A[N-1],A[midx])