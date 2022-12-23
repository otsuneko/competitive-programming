N,X,Y = map(int,input().split())
A = list(map(int,input().split()))

cand_y = [set() for _ in range(2*abs(X)+1)]
print(cand_y)

# 0:スタート,1:x方向,2:y方向
cand_y[X].add((0,0,0))
cand_y[X+A[0]].add((1,0,1))

for x in range(2*abs(X)+1):
    for n,y,dir in cand_y[x]:
        # X方向に右に伸ばす
        if dir == 2 and X >= 0 and x+A[n] <= 2*X:
            cand_y[x+A[n]].add((n+1,y,1))

        # X方向に左に伸ばす
        if dir == 2 and X < 0 and x-A[n] >= 2*X:
            cand_y[x+A[n]].add((n+1,y,1))

        # Y方向に右に伸ばす
        if dir == 1 and Y >= 0 and y+A[n] <= Y:
            cand_y[x].add((n+1,y+A[n],2))

        # Y方向に左に伸ばす
        if dir == 1 and Y < 0 and y-A[n] >= Y:
            cand_y[x].add((n+1,y+A[n],2))

for n,y,dir in cand_y[2*X]:
    if n == N and y == 2*Y:
        print("Yes")
        exit()
print("No")