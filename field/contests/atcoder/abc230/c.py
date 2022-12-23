N,A,B = map(int,input().split())
P,Q,R,S = map(int,input().split())

masu = [["."]*(S-R+1) for _ in range(Q-P+1)]

mi,ma = max(P-A, R-B), min(Q-A, S-B)
for k in range(mi,ma+1):
    masu[A-P+k][B-R+k] = "#"

mi,ma = max(P-A, B-S), min(Q-A, B-R)
for k in range(mi,ma+1):
    masu[A-P+k][B-R-k] = "#"

# K = max((S-R+1), (Q-P+1))
# for k in range(-K,K+1):
#     if 0 <= (A-P+k) < (Q-P+1) and 0 <= (B-R+k) < (S-R+1):
#         masu[A-P+k][B-R+k] = "#"
#     if 0 <= (A-P+k) < (Q-P+1) and 0 <= (B-R-k) < (S-R+1):
#         masu[A-P+k][B-R-k] = "#"

for i in range(Q-P+1):
    print("".join(masu[i]))
