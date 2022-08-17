import itertools

N,M = map(int,input().split())
rel = set()
for _ in range(M):
    x,y =map(int,input().split())
    x,y = x-1,y-1
    rel.add((x,y))

ans = 0
for bit in itertools.product([True, False], repeat=N):

    member = [i for i,b in enumerate(bit) if b]

    for c in itertools.combinations(member,2):
        if (c[0],c[1]) not in rel:
                break
    else:
        ans = max(ans, len(member))

print(ans)