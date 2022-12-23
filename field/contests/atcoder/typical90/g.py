import bisect
N = int(input())
A = list(map(int,input().split()))
A.sort()
Q = int(input())
for _ in range(Q):
    B = int(input())
    idx = bisect.bisect_left(A,B)
    idx = idx - 1 if idx == N else idx
    idx_l = idx - 1 if idx > 0 else idx
    print(min(abs(B-A[idx_l]), abs(B-A[idx])))