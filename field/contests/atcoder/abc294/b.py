alphabet = "abcdefghijklmnopqrstuvwxyz"
H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]

ans = [[] for _ in range(H)]

for h in range(H):
    for w in range(W):
        if A[h][w] == 0:
            ans[h].append(".")
        else:
            ans[h].append((alphabet[A[h][w]-1]).upper())

for h in range(H):
    print("".join(ans[h]))