import itertools
N,M,X = map(int,input().split())
books = [list(map(int,input().split())) for _ in range(N)]

ans = 10**18
for bit in range(1<<N):

    cost = 0
    skills = [0]*M
    for i in range(N):
        if bit & 1<<i:
            cost += books[i][0]
            for j in range(M):
                skills[j] += books[i][j+1]
    
    for skill in skills:
        if skill < X:
            break
    else:
        ans = min(ans, cost)

if ans == 10**18:
    print(-1)
else:
    print(ans)