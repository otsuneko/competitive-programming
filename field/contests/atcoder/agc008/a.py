x,y = map(int,input().split())

if y > x:
    if x*y >= 0:
        print(y-x)
    else:
        if y > abs(x):
            print(1 + y - abs(x))
        else:
            print(abs(x)-y + 1)
elif y == x:
    print(0)
else:
    if x*y > 0:
        print(2 + x-y)
    elif x == 0:
        print(abs(y) + 1)
    elif y == 0:
        print(1 + x)
    elif abs(y) >= x:
        print(abs(y) - x + 1)
    else:
        print(1 + x - abs(y))