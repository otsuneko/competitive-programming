W,a,b = map(int,input().split())

if b > a:
    if b > a+W:
        print(b-a-W)
    else:
        print(0)
elif b == 0:
    print(0)
else:
    if a > b+W:
        print(a-b-W)
    else:
        print(0)