N = int(input())
A = [list(input()) for _ in range(N)]

ans = True
for i in range(N):
    for j in range(N):
        if i == j:
            if A[i][j] != "-":
                ans = False
        elif A[i][j] == "W" and A[j][i] != "L":
            ans = False
        elif A[i][j] == "L" and A[j][i] != "W":
            ans = False
        elif A[i][j] == "D" and A[j][i] != "D":
            ans = False
print(["incorrect","correct"][ans])