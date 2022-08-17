N = int(input())
pos = [list(map(int,input().split())) for _ in range(N)]

ans = 0
for i in range(N):
    for j in range(i+1,N):
        for k in range(j+1,N):
            p = [pos[i],pos[j],pos[k]]
            p.sort()
            x1,y1 = p[0]
            x2,y2 = p[1]
            x3,y3 = p[2]

            if (x3-x1)*(y2-y1) == (x2-x1)*(y3-y1):
                continue
            else:
                ans += 1
print(ans)