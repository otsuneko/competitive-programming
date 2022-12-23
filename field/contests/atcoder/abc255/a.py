R,C = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(R)]

print(A[R-1][C-1])