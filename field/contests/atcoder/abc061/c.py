N,K = map(int,input().split())
li = []
for _ in range(N):
    a,b = map(int,input().split())
    li.append((a,b))

li.sort()

cnt = 0
for i in range(N):
    cnt += li[i][1]
    if cnt >= K:
        print(li[i][0])
        break