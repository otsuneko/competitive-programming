N = int(input())
A = list(map(int,input().split()))
X = int(input())
sum_A = sum(A)

ans = X//sum_A * N
total = X//sum_A * sum_A

if total > X:
    print(ans)
    exit()

for i in range(N):
    total += A[i]
    if total > X:
        ans += i+1
        print(ans)
        exit()
