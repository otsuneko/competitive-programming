N = int(input())
D = [list(map(int,input().split())) for _ in range(N)]

cnt = 0
for d in D:
    if d[0] == d[1]:
        cnt += 1
    else:
        cnt = 0
    
    if cnt == 3:
        print("Yes")
        exit()
print("No")