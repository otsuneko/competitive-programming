import time
import random

sx,sy = map(int,input().split())
tx,ty = map(int,input().split())
a,b,c,d = map(int,input().split())

start = time.time()
ans = []
while 1:
    now = time.time()
    if now - start > 1.9:
        break
    
    rx = random.randint(a,b)
    ry = random.randint(c,d)
    ans.append((rx,ry))

    sx = rx*2 - sx
    sy = ry*2 - sy

    if a <= (sx+tx)/2 <= b and c <= (sy+ty)/2 <= d:
        print("Yes")
        for pos in ans:
            print(*pos)
        exit()

print("No")