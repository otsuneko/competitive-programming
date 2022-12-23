H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
T = [list(input()) for _ in range(H)]

S = list(zip(*S))
T = list(zip(*T))

S.sort()
T.sort()

if S == T:
    print("Yes")
else:
    print("No")