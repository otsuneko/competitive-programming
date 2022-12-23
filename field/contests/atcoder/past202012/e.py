def rotate(T, angle):
    new_T = [[""]*W for i in range(H)]
    if angle == 90:
        for i in range(H):
            for j in range(W):
                new_T[i][j] = T[H-j-1][i]
    elif angle == 180:
        for i in range(H):
            for j in range(W):
                new_T[i][j] = T[H-1-i][W-1-j]
    return new_T

def check(S,T):
    for i in range(H):
        for j in range(W):
            if S[i][j] == "#" and T[i][j] == "#":
                return False
    return True

H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
T = [list(input()) for _ in range(H)]

if H == W:
    new_T = T
    flag = False
    for i in range(4):
        new_T = rotate(new_T,90)
        for j in range(H):
            if new_T[j].count(".") == len(new_T[j]):
                new_T2 = new_T[]
        if check(S,new_T):
            print("Yes")
            break
    else:
        print("No")
else:
    new_T = T
    for i in range(2):
        new_T = rotate(new_T,180)
        if check(S,new_T):
            print("Yes")
            break
    else:
        print("No")