N,M,X,Y = map(int,input().split())
x = list(map(int,input().split()))
y = list(map(int,input().split()))

maX = max(x)
miY = min(y)

if X < maX < miY <= Y:
    print("No War")
else:
    print("War")