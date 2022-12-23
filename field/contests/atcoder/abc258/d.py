N,X = map(int,input().split())
games = [list(map(int,input().split())) for _ in range(N)]

ans = 10**19
miB = 10**18
time = 0
cnt = 0
for watch,play in games:
    time += watch
    time += play
    cnt += 1
    miB = min(miB, play)
    ans = min(ans, time + miB*(X-cnt))
print(ans)