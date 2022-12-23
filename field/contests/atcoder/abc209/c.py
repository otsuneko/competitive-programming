N = int(input())
C = list(map(int,input().split()))
C.sort()
# print(C)
mod = 10**9+7

ans = 1
prev = 0
for i in range(N):
    if i == 0:
        ans = ans*C[i]%mod
    else:
        ans = ans*(C[i]-i)%mod
    prev = C[i]
    # print(ans)

print(ans)