H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]

for h_s in range(H):
    for h_t in range(h_s+1,H):
        for w_s in range(W):
            for w_t in range(w_s+1, W):
                if A[h_s][w_s] + A[h_t][w_t] > A[h_s][w_t] + A[h_t][w_s]:
                    print("No")
                    exit()
print("Yes")