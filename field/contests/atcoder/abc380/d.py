import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()
N = len(S)
Q = int(input())
K = list(map(int,input().split()))

ans = []
for k in K:
    idx = k%N

    k -= idx

    flg = True
    cur = 0
    while cur != k:
        if cur*2 < k:
            cur *= 2
            flg = not flg
        elif cur == 0:
            cur += N
            flg = not flg
        else:
            cur += cur/2
            flg = not flg


    if flg:
        ans.append(S[idx-1])
    else:
        if S[idx-1].islower():
            ans.append(S[idx-1].upper())
        else:
            ans.append(S[idx-1].lower())
print(*ans)
