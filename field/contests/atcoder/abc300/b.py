import copy
def rolling(s, n):
    l = len(s)
    #右にシフトの場合
    return s[n%l:] + s[:n%l] #左にシフトの場合はnの正負を逆に

H,W = map(int,input().split())
A = [list(input()) for _ in range(H)]
B = [list(input()) for _ in range(H)]

for s in range(H):
    inv = list(zip(*A))
    for w1 in range(W):
        inv[w1] = rolling(inv[w1],s+1)
    A2 = list(zip(*inv))
    # print(*A2, sep="\n")
    for t in range(W):
        for h2 in range(H):
            A2[h2] = rolling(A2[h2],1)
        for y in range(H):
            for x in range(W):
                if A2[y][x] != B[y][x]:
                    break
            else:
                continue
            break
        else:
            print("Yes")
            exit()
print("No")
