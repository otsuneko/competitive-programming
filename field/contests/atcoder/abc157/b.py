A = [list(map(int,input().split())) for _ in range(3)]
N = int(input())
B = [int(input()) for _ in range(N)]

card = [[False]*3 for _ in range(3)]
for b in B:
    for i in range(3):
        for j in range(3):
            if b == A[i][j]:
                card[i][j] = True

for i in range(3):
    if card[0][i] == card[1][i] == card[2][i] == True or card[i][0] == card[i][1] == card[i][2] == True:
        print("Yes")
        exit()

if card[0][0] == card[1][1] == card[2][2] == True or card[2][0] == card[1][1] == card[0][2] == True:
    print("Yes")
    exit()

print("No")