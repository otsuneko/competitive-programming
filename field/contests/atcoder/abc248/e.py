def calc_linear(x1,y1,x2,y2):
    dy = (y2-y1)
    dx = (x2-x1)
    bup = x2*y1 - x1*y2
    bbottom = x2-x1
    return (dy,dx,bup,bbottom)

N,K =map(int,input().split())
pos =[tuple(map(int,input().split())) for _ in range(N)]

if K == 1:
    print("Infinity")
    exit()

s = set()
s_x = set()
s_y = set()
for i,(x1,y1) in enumerate(pos):
    for j,(x2,y2) in enumerate(pos):
        if i == j:
            continue
        if x1 == x2:
            cnt2 = 0
            for x,y in pos:
                if x == x1:
                    cnt2 += 1
            if cnt2 >= K:
                s_x.add(x1)
            continue
        elif y1 == y2:
            cnt2 = 0
            for x,y in pos:
                if y == y1:
                    cnt2 += 1
            if cnt2 >= K:
                s_y.add(y1)
            continue
        dy,dx,bup,bbottom = calc_linear(x1,y1,x2,y2)
        cnt = 0
        for x,y in pos:
            if y == (dy/dx)*x + b:
                cnt += 1
        if cnt >= K:
            s.add((a,b))

print(len(s)+len(s_x)+len(s_y))