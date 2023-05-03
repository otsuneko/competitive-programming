# 二次元配列の90度右回転
def rotate_2d(arr):
    return zip(*arr[::-1])

N = int(input())
A = [list(map(int,input().split())) for _ in range(N)]
B = [list(map(int,input().split())) for _ in range(N)]

for i in range(4):
    A = list(rotate_2d(A))

    ans = True
    for y in range(N):
        for x in range(N):
            if A[y][x] == 1 and B[y][x] != 1:
                ans = False
                break
        else:
            continue
        break
    if ans:
        print("Yes")
        exit()
print("No")