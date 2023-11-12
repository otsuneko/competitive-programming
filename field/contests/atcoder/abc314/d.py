import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = input()
Q = int(input())

que = []
for _ in range(Q):
    t,x,c = map(str,input().split())
    que.append((t,x,c))

flg = -1
last_idx = INF
for i in range(Q-1,-1,-1):
    t,x,c = que[i]
    t,x = int(t),int(x)
    match t:
        case 2:
            flg = 0
            last_idx = i
            break
        case 3:
            flg = 1
            last_idx = i
            break

if flg == 0:
    ans = list(S.lower())
elif flg == 1:
    ans = list(S.upper())
else:
    ans = list(S)

for i in range(Q):
    t,x,c = que[i]
    t,x = int(t),int(x)
    x -= 1
    if t == 1:
        if i <= last_idx:
            if flg == -1:
                ans[x] = c
            elif flg == 0:
                ans[x] = c.lower()
            else:
                ans[x] = c.upper()
        else:
            ans[x] = c

print("".join(ans))