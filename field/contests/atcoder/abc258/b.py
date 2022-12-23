N = int(input())
A = [list(input()) for _ in range(N)]

ans = 0
move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
for y in range(N):
    for x in range(N):
        for dy,dx in move:
            tmp = ""
            for k in range(1,N+1):
                ny,nx = y + dy*k, x + dx*k
                if ny < 0:
                    ny += N
                elif ny >= N:
                    ny -= N
                if nx < 0:
                    nx += N
                elif nx >= N:
                    nx -= N
                # print(ny,nx)
                tmp += A[ny][nx]
            ans = max(ans,int(tmp))
print(ans)