N,Q = map(int,input().split())
cards = [0]*N

for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        x = query[1]-1
        cards[x] += 1
    elif query[0] == 2:
        x = query[1]-1
        cards[x] += 2
    elif query[0] == 3:
        x = query[1]-1
        if cards[x] >= 2:
            print("Yes")
        else:
            print("No")