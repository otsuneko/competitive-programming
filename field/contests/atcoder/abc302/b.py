H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

DIR = [(-1,-1),(-1,0),(1,0),(1,1),(0,1),(0,-1),(1,-1),(-1,1)]
snuke = ["s","n","u","k","e"]
for y in range(H):
    for x in range(W):
        if S[y][x] != snuke[0]:
            continue
        for dy,dx in DIR:
                ans = [(y+1,x+1)]
                for i in range(1,5):
                    ny,nx = y+dy*(i),x+dx*(i)
                    if not (0<=ny<H and 0<=nx<W and S[ny][nx] == snuke[i]):
                        break
                    ans.append((ny+1,nx+1))
                else:
                    for y,x in ans:
                        print(y,x)
                    exit()