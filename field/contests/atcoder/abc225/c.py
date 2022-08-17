N,M = map(int,input().split())
B = [list(map(int,input().split())) for _ in range(N)]

flg = True
for i in range(N):
    for j in range(M):
        if i == 0 and j == 0:
            continue
        elif i == 0:
            if B[i][j] != B[i][j-1] + 1:
                flg = False        
        elif j == 0:
            if B[i][j] != B[i-1][j] + 7:
                flg = False        
        else:
            if B[i][j] != B[i][j-1] + 1 or B[i][j] != B[i-1][j] + 7:
                flg = False
        
        if B[i][j]%7==0 and j != M-1:
            flg = False

print(["No","Yes"][flg])