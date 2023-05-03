N,T = map(int,input().split())
C = list(map(int,input().split()))
R = list(map(int,input().split()))

flg = False
if T in C:
    flg = True
ma = 0
ans = 1
for i in range(N):
    if flg and C[i] == T:
        if R[i] > ma:
            ma = R[i]
            ans = i+1
    elif not flg and C[i] == C[0]:
        if R[i] > ma:
            ma = R[i]
            ans = i+1

print(ans)