X,Y,N = map(int,input().split())

if 3*X > Y:
    print(N//3*Y + N%3*X)
else:
    print(X*N)