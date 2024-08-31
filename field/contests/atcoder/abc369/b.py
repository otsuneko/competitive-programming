import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
hands = [list(map(str,input().split())) for _ in range(N)]

ans = 10**18
for l in range(101):
    for r in range(101):
        tmp = 0
        cur_l = l
        cur_r = r
        for i in range(N):
            a = int(hands[i][0])
            if hands[i][1] == "L":
                tmp += abs(cur_l-a)
                cur_l = a
            else:
                tmp += abs(cur_r-a)
                cur_r = a
        if tmp < ans:
            ans = tmp
print(ans)
