N,K = map(int,input().split())
A = list(map(int,input().split()))
pos = [list(map(int,input().split())) for _ in range(N)]

person = [10**18]*N

for a in A:
    person[a-1] = 0
    for i,(x1,y1) in enumerate(pos):
        if i == a-1:
            continue
        x2,y2 = pos[a-1]
        person[i] = min(person[i],((x1-x2)**2 + (y1-y2)**2)**0.5)
    
print(max(person))