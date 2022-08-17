H,W = map(int,input().split())

if H == 1 or W == 1:
    print(1)
elif H%2 == 1 and W%2 == 1:
    print(max(H*W//2, H*W-H*W//2))
else:
    print(H*W//2)