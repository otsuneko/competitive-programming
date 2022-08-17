x,y = map(int,input().split())

s = set([0,1,2])
if x == y:
    print(x)
else:
    s2 = s-set([x,y])
    print(*s2)