N,L =map(int,input().split())
tents =[list(map(int,input().split())) for _ in range(N)]

ans = 0
hp = 0
pre = L
for i in reversed(range(N)):
    if hp < pre-tents[i][0]:
        hp = 0
    else:
        hp -= pre-tents[i][0]
    pre = tents[i][0]
    hp += tents[i][1]
    
    ans = max(ans, hp)

print(ans)