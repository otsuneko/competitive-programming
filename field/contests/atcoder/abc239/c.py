x1,y1,x2,y2 =map(int,input().split())

ans = False
for x in range(x1-10,x1+10):
    for y in range(y1-10,y1+10):
        if (x-x1)**2+(y-y1)**2 == 5 and (x-x2)**2+(y-y2)**2 == 5:
            ans = True

print(["No","Yes"][ans])