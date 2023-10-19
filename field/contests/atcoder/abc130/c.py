def linear_func(y1,x1,y2,x2):
    a = (y2-y1)/(x2-x1)
    b = y1-a*x1
    return a,b

W,H,x,y = map(int,input().split())

ans = 0
flg = 0
if x*2 == W and y*2 == H:
    ans = H*W/2
    flg = 1
    print(ans,flg)
    exit()

cy,cx = H/2,W/2
if x == cx:
    ans = H*W/2
    print(ans,flg)
    exit()

a,b = linear_func(y,x,cy,cx)

if not 0<=b<=H:
    x0 = -b/a
    xH = (H-b)/a
    ans = abs(xH-x0)*H/2 + min(xH,x0)*H
else:
    y0 = b
    yW = a*W + b
    ans = abs(yW-y0)*W/2 + min(yW,y0)*W
print(ans,flg)