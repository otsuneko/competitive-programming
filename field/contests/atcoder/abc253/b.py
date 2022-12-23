H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

pos = []
for h in range(H):
    for w in range(W):
        if S[h][w] == "o":
            pos.append([h,w])

print(abs(pos[0][0]-pos[1][0]) + abs(pos[0][1]-pos[1][1]))