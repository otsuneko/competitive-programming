H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]

H_sum = [0]*H
W_sum = [0]*W
for i in range(H):
    H_sum[i] = sum(A[i])

inv = list(zip(*A))
for i in range(W):
    W_sum[i] = sum(inv[i])

for i in range(H):
    B = []
    for j in range(W):
        B.append(H_sum[i]+W_sum[j]-A[i][j])
    print(*B)