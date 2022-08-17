H,W =map(int,input().split())
R,C =map(int,input().split())

ans = 0
if 1 < R < H:
    ans += 2
elif R < H or 1 < R:
    ans += 1

if 1 < C < W:
    ans += 2
elif C < W or 1 < C:
    ans += 1

print(ans)