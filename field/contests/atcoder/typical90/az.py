N = int(input())
A = [list(map(int,input().split())) for _ in range(N)]

ans = 0
product = A[0][:]
for i in range(N-1):
    for j in range(6):
        product[j] = product[j] * sum(A[i+1])
print(sum(product)%(10**9+7))