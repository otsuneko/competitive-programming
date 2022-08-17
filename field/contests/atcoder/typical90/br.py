N =int(input())

pos = []
posx = []
posy = []
for _ in range(N):
    x,y =map(int,input().split())
    pos.append([x,y])
    posx.append(x)
    posy.append(y)

posx.sort()
posy.sort()
med = [posx[N//2],posy[N//2]]

ans = 0
for x,y in pos:
    ans += abs(med[0]-x) + abs(med[1]-y)

print(ans)