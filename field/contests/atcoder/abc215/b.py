import math
N = int(input())

K = int(math.log2(N))

ans = 0
for i in range(K-2,K+3):
    if 2**i <= N:
        ans = i
print(ans)