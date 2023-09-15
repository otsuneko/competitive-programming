import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys
sys.setrecursionlimit(10**7)

MOD = 10**9+7
def mex(a,b,c):
    for i in range(3):
        if all([a != i, b != i, c != i]):
            return i
    return 3

N = int(input())
A = list(map(int,input().split()))
S = input()

# S[i] == "M"　かつ A[i] == "0"~"2"の数をカウント
cnt_M = [[0]*N for _ in range(3)]
# S[i] == "X"　かつ A[i] == "0"~"2"の数をカウント
cnt_X = [[0]*N for _ in range(3)]
for i in range(N):
    if S[i] == "M":
        cnt_M[A[i]][i] = 1
    elif S[i] == "X":
        cnt_X[A[i]][i] = 1

# cnt_Mとcnt_Xそれぞれについて累積和をとる
import itertools
import operator
cumsum_M = []
cumsum_X = []
for i in range(3):
    cumsum = [0] + list(itertools.accumulate(cnt_M[i], func=operator.add))
    cumsum_M.append(cumsum)

    cumsum = list(itertools.accumulate(cnt_X[i][::-1], func=operator.add))[::-1] + [0] # 逆順の累積和
    cumsum_X.append(cumsum)

# print(cumsum_M)
# print(cumsum_X)

ans = 0
for i in range(N):
    if S[i] != "E":
        continue
    for j in range(3):
        for k in range(3):
            ans += cumsum_M[j][i] * cumsum_X[k][i+1] * mex(j, A[i], k)

print(ans)