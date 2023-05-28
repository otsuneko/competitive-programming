N,M = map(int,input().split())
cnt_one,cnt_M = 0,0
start = []
goal = []
middle = []
for _ in range(N):
    A = int(input())
    s = set(map(int,input().split()))
    if 1 in s and M in s:
        print(0)
        exit()
    elif 1 in s:
        start.append(s)
        cnt_one += 1
    elif M in s:
        goal.append(s)
        cnt_M += 1
    else:
        middle.append(s)

if [cnt_one,cnt_M] == [0,0]:
    print(-1)
    exit()

ans = 10**18
memo = dict()
for s in start:
    for g in goal:
        