N = int(input())
pyr = [list(map(int,input().split())) for _ in range(N)]

H = 10**9
for cx in range(0,101):
    for cy in range(0,101):
        for i in range(N):
            x1,y1,h1 = pyr[i]
            H = h1 + abs(x1-cx) + abs(y1-cy)

            for j in range(N):
                if i == j:
                    continue
                x1,y1,h1 = pyr[j]
                if max(H - abs(x1-cx) - abs(y1-cy),0) != h1:
                    break
            else:
                print(cx,cy,H)
                exit()
