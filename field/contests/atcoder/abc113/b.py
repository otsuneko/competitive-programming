N = int(input())
T,A = map(int,input().split())
H = list(map(int,input().split()))

palace = []
ans = 0
min_diff = 10**18
for i in range(N):
    degree = T - H[i]*0.006
    palace.append(degree)
    if abs(A - degree) < min_diff:
        ans = i+1
        min_diff = abs(A - degree)

print(ans)