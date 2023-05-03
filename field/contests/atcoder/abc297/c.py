H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

for y in range(H):
    for x in range(W-1):
        if S[y][x] == S[y][x+1] == "T":
            S[y][x] = "P"
            S[y][x+1] = "C"

for y in range(H):
    print("".join(S[y]))