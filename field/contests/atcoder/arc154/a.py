N = int(input())
A = list(input())
B = list(input())

mod = 998244353

diff = int("".join(B)) - int("".join(A))
ans = int("".join(B)) * int("".join(A))

for i in range(N):
    A[i],B[i] = B[i],A[i]
    if abs(int("".join(B)) - int("".join(A))) > diff:
        ans = int("".join(A)) * int("".join(B))

print(ans%mod)