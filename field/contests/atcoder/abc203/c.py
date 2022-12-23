N,K = map(int,input().split())

friend = []
for _ in range(N):
    friend.append(list(map(int,input().split())))

friend.sort()

now = 0
for f in friend:
    if K < f[0]-now:
        print(K+now)
        exit()
    K -= f[0]-now
    K += f[1]
    now = f[0]
    # print(now,K)
print(K+now)