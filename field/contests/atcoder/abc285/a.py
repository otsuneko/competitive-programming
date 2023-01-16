a,b = map(int,input().split())

if a > b:
    a,b = b,a

if b in [a*2,a*2+1]:
    print("Yes")
else:
    print("No")