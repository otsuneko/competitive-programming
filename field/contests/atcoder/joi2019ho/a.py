import sys
input = lambda: sys.stdin.readline().rstrip()
H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

#[O,I]
cnt = {}
for y in range(H):
    cnt[(W-1) + y*W] = [1,0] if S[y][W-1] == "O" else [0,0]
for x in range(W):
    cnt[x + (H-1)*W] = [0,1] if S[H-1][x] == "I" else [0,0]

ans = 0
for y in reversed(range(H-1)):
    for x in reversed(range(W-1)):
        idx = x + y*W
        if S[y][x] == "J":
            cnt[idx] = [cnt[idx+1][0],cnt[idx+W][1]]
            ans += cnt[idx][0] * cnt[idx][1]
        elif S[y][x] == "O":
            cnt[idx] = [cnt[idx+1][0] + 1, cnt[idx+W][1]]
        elif S[y][x] == "I":
            cnt[idx] = [cnt[idx+1][0], cnt[idx+W][1] + 1]
print(ans)