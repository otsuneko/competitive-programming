N,M = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
# C = A + B
# C.sort()
# A2 = set(A)
# B2 = set(B)

# ans = 10**18
# for i in range(N+M-1):
#     if C[i+1]-C[i] < ans and ((C[i+1] in A2 and C[i] in B2) or (C[i] in A2 and C[i+1] in B2)):
#         ans = C[i+1]-C[i]
# print(ans)

import bisect

ans = 10**18

B.sort()
for a in A:
    idx = bisect.bisect(B,a)
    ans = min(ans, abs(a - B[max(0,idx-1)]), abs(a - B[min(M-1,idx)]))

print(ans)