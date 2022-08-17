N,M = map(int,input().split())

if M < N*2 or M > 4*N:
    print("-1 -1 -1")
    exit()

ans = [0,0,0]
for z in range(10**5+1):
    y = M - 2*N - 2*z
    x = N - y - z
    if x >= 0 and y >= 0:
        print(x,y,z)
        exit()
print("-1 -1 -1")