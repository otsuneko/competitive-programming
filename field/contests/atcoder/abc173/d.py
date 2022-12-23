N = int(input())
A = list(map(int,input().split()))

A.sort(reverse=True)

ans = A[0]

idx = 1
for i in range(1,N-1):
    ans += A[idx]
    if i%2 == 0:
        idx += 1

print(ans)