import bisect

class Rect:
  def __init__(self, H, W):
    self.H = H
    self.W = W

import bisect
N,M =map(int,input().split())
A =list(map(int,input().split()))
B =list(map(int,input().split()))
C =list(map(int,input().split()))
D =list(map(int,input().split()))

CHOCO = [Rect(A[i],B[i]) for i in range(N)]
CHOCO.sort(key = lambda b: b.W, reverse = True)
CHOCO.sort(key = lambda b: b.H)

BOX = [Rect(C[i],D[i]) for i in range(M)]
BOX.sort(key = lambda b: b.W, reverse = True)
BOX.sort(key = lambda b: b.H)


dp = [CHOCO[0].W]
for choco in CHOCO:
  if dp[-1] < choco.W:
    dp.append(choco.W)
  else:
    dp[bisect.bisect_left(dp, box.W)] = box.W
print(dp)

# choco = []
# for i in range(N):
#     choco.append([A[i],B[i]])

# box = []
# for i in range(M):
#     box.append([C[i],D[i]])

# choco = sorted(choco, key = lambda x: (x[0],-x[1]))
# box = sorted(choco, key = lambda x: (x[0],-x[1]))

# dp = [10**18] * (N+1)
# for k in range(N):
#     dp[bisect.bisect_left(dp, hako2[k])] = hako2[k]

# ans = 0
# for k in range(N+1):
#     if dp[k] < 10**18:
#         ans = k+1
# print(ans)


# from bisect import bisect

# # N: 数列の長さ
# # A[i]: a_i の値
# def LIS(N, A):
#     INF = 10**10

#     dp = [INF]*(N+1)
#     dp[0] = -1
#     for a in A:
#         #idx = bisect(dp, a) #広義最長増加部分列
#         idx = bisect(dp, a-1) 
#         dp[idx] = min(a, dp[idx])
#     return max(i for i in range(N+1) if dp[i] < INF)