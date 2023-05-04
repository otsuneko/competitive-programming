S = [list(input()) for _ in range(8)]

alpha = "abcdefghijklmnopqrstuvwxyz"

for y in range(8):
    for x in range(8):
        if S[y][x] == "*":
            print(alpha[x] + str(8-y))
            exit()