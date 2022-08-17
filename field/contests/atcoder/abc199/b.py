N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

l = 0
r = float("INF")
for i in range(N):
    l = max(l, A[i])
    r = min(r, B[i])
if l <= r:
    print(r-l+1)
else:
    print(0)