#AtCoder
m = int(input())
zodiac = [tuple(map(int,input().split())) for _ in range(m)]

base = zodiac[0]
rel_pos = []
for i in range(1,m):
    rel_pos.append([zodiac[i][0]-base[0], zodiac[i][1]-base[1]])

n = int(input())
stars = [tuple(map(int,input().split())) for _ in range(n)]

for s in stars:
    for r in rel_pos:
        if (s[0] + r[0], s[1] + r[1]) not in stars:
            break
    else:
        print(s[0]-zodiac[0][0], s[1] - zodiac[0][1])
        break

#AOJ
while 1:
    m = int(input())
    if not m:
        break
    zodiac = [tuple(map(int,input().split())) for _ in range(m)]

    base = zodiac[0]
    rel_pos = []
    for i in range(1,m):
        rel_pos.append([zodiac[i][0]-base[0], zodiac[i][1]-base[1]])

    n = int(input())
    stars = [tuple(map(int,input().split())) for _ in range(n)]

    for s in stars:
        for r in rel_pos:
            if (s[0] + r[0], s[1] + r[1]) not in stars:
                break
        else:
            print(s[0]-zodiac[0][0], s[1] - zodiac[0][1])
            break
            