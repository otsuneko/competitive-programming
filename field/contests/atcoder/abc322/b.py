import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
S = input()
T = input()

cnt_pre = cnt_suf = 0
for i in range(N):
    if S[i] == T[i]:
        cnt_pre += 1
    if S[i] == T[M-N+i]:
        cnt_suf += 1
# print(cnt_pre,cnt_suf)
if cnt_pre == cnt_suf == N:
    print(0)
elif cnt_pre == N:
    print(1)
elif cnt_suf == N:
    print(2)
else:
    print(3)