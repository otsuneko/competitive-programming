H,W = map(int,input().split())

if H > 1 and W > 1 or H == W == 1:
    print(((H+1)//2) * ((W+1)//2))
else:
    if H > W:
        print(H)
    else:
        print(W)