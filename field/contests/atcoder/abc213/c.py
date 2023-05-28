# 引数となるリストはソート不要かつ値の重複可(内部処理で対応するため)
def compress(arr):
    *XS, = set(arr)
    XS.sort()
    return {e: i for i, e in enumerate(XS)}

H,W,N = map(int,input().split())
cards = []
row,col = [],[]
for _ in range(N):
    card = list(map(int,input().split()))
    cards.append(card)
    row.append(card[0])
    col.append(card[1])

row2 = compress(row)
col2 = compress(col)
# print(row2,col2)

for y,x in cards:
    print(row2[y],col2[x])