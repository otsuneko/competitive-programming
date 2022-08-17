A,B,C,D = map(int,input().split())
inf = 10**18

ans = 0
mizu = A
aka = 0

if A+(B*inf) > C*inf*D:
    print(-1)
    exit()

while 1:
    if mizu <= aka*D:
        break
    mizu += B
    aka += C
    ans += 1

print(ans)