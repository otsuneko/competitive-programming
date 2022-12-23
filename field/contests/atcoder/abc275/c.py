S = [list(input()) for _ in range(9)]
# print(*S, sep="\n")

cnt = set()

pawn = []
for r in range(9):
    for c in range(9):
        if S[r][c] == "#":
            pawn.append((r,c))

for i in range(len(pawn)):
    r1,c1 = pawn[i]
    for j in range(i+1,len(pawn)):
        r2,c2 = pawn[j]
        dy,dx = r2-r1,c2-c1
        
        #片側
        dy2,dx2 = -dx,dy
        r3,c3 = r1+dy2,c1+dx2
        r4,c4 = r2+dy2,c2+dx2
        if (r3,c3) in pawn and (r4,c4) in pawn:
            tmp = [(r1,c1),(r2,c2),(r3,c3),(r4,c4)]
            # 昇順降順を入れ替える場合はlambda式の正負を反転
            tmp.sort(key=lambda x:(x[0],x[1]))
            cnt.add(tuple(tmp))

        #もう片側
        dy2,dx2 = dx,-dy
        r3,c3 = r1+dy2,c1+dx2
        r4,c4 = r2+dy2,c2+dx2
        if (r3,c3) in pawn and (r4,c4) in pawn:
            tmp = [(r1,c1),(r2,c2),(r3,c3),(r4,c4)]
            # 昇順降順を入れ替える場合はlambda式の正負を反転
            tmp.sort(key=lambda x:(x[0],x[1]))
            cnt.add(tuple(tmp))

# print(cnt)
print(len(cnt))