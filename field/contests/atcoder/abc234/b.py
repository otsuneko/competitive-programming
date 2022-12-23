N =int(input())
pos =[list(map(int,input().split())) for _ in range(N)]

ans = 0
for i in range(N):
    for j in range(N):
        l = (pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2

        ans = max(ans, l)

print(ans**0.5)