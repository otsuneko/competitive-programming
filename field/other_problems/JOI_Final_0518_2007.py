while 1:
    N = int(input())
    if not N:
        break

    pillars = []
    for _ in range(N):
        x,y = map(int,input().split())
        pillars.append((x,y))

    pillars.sort(key=lambda x:(x[1],x[0]))
    check = set(pillars)
    
    ans = 0
    for i in range(N):
        for j in range(i+1,N):
            x1,y1 = pillars[i]
            x2,y2 = pillars[j]
            if x1 < x2:
                dx = x2-x1
                dy = y2-y1
                x3,y3 = x1 - dy, y1 + dx
                x4,y4 = x2 - dy, y2 + dx
            else:
                dx = x1-x2
                dy = y2-y1
                x3,y3 = x1 + dy, y1 + dx
                x4,y4 = x2 + dy, y2 + dx
            if (x3,y3) in check and (x4,y4) in check:
                area = dx**2 + dy**2
                ans = max(ans,area)
    print(ans)
