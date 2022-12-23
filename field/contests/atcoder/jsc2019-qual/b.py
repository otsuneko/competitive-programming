mod = 10**9+7
N,K = map(int,input().split())
A = list(map(int,input().split()))

inv = [0]*N
for i in range(N-1):
    for j in range(i+1,N):
        if A[i] > A[j]:
            inv[i] += 1

A2 = A*2
inv2 = [0]*N
for i in range(N):
    for j in range(i+1,2*N):
        if A2[i] > A2[j]:
            inv2[i] += 1

a = sum(inv)
d = sum(inv2)-a

ans = (a + a+d*(K-1)) * K // 2 % mod
print(ans)