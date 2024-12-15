import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,Q = map(int,input().split())
S = list(input())

flg = [0]*N
ans = 0
for i in range(N-2):
    if "".join(S[i:i+3]) == "ABC":
        flg[i] = flg[i+1] = flg[i+2] = 1
        ans += 1

for _ in range(Q):
    X,C = map(str,input().split())
    X = int(X)-1

    if S[X] == C:
        print(ans)
        continue

    if flg[X] == 1:
        if S[X] == "A":
            flg[X] = flg[X+1] = flg[X+2] = 0
        elif S[X] == "B":
            flg[X-1] = flg[X] = flg[X+1] = 0
        elif S[X] == "C":
            flg[X-2] = flg[X-1] = flg[X] = 0
        ans -= 1
    S[X] = C

    if S[X] == "A" and "".join(S[X:X+3]) == "ABC":
        flg[X] = flg[X+1] = flg[X+2] = 1
        ans += 1
    elif S[X] == "B" and "".join(S[X-1:X+2]) == "ABC":
        flg[X-1] = flg[X] = flg[X+1] = 1
        ans += 1
    elif S[X] == "C" and "".join(S[X-2:X+1]) == "ABC":
        flg[X-2] = flg[X-1] = flg[X] = 1
        ans += 1
    print(ans)
