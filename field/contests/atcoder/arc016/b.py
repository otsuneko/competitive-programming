N = int(input())
fumen = [list(input()) for _ in range(N)]

# print(*fumen, sep="\n")

ans = 0
for i in range(N):
    for j in range(9):
        if fumen[i][j] == "x":
            ans += 1
        elif fumen[i][j] == "o":
            if i == 0:
                ans += 1
            elif fumen[i-1][j] != "o":
                ans += 1

print(ans)