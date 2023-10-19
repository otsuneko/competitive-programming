import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
N,K,P = map(int,input().split())
CA = [list(map(int,input().split())) for _ in range(N)]

from collections import defaultdict
dp = defaultdict(lambda: INF)
dp[tuple([0]*K)] = 0

for C,*A in CA:
    ndp = defaultdict(lambda: INF)
    for prms,cost in dp.items():
        nprms = []
        for k in range(K):
            nprms.append(min(P,prms[k] + A[k]))
        nprms = tuple(nprms)
        ndp[nprms] = min(ndp[nprms],cost+C)
    for prms,cost in ndp.items():
        dp[prms] = min(dp[prms],cost)

if dp[tuple([P]*K)] == INF:
    print(-1)
else:
    print(dp[tuple([P]*K)])

# # 10進数⇒n進数(返り値リスト)
# def base10int_list(value, base):
#     upper = value >= base and base10int_list(value // base, base) or []
#     return upper + [value % base]  # リストの結合

# def decode(digits, base):
#     value = 0
#     for digit in digits:
#         value = value * base + int(digit)
#     return value

# # 現状のステータスと案の効果をもとに次のステータスを計算
# def translate(cur,up):
#     # 各パラメータの現在のステータス計算
#     cur_param = base10int_list(cur,P+1)

#     for i in range(len(cur_param)):
#         up[i] = min(P,up[i]+cur_param[i])

#     return decode(up,P+1)

# dp = [[INF]*(P+1)**K for _ in range(N+1)]
# dp[0][0] = 0

# for i in range(N):
#     for j in range((P+1)**K):
#         # 実行する場合
#         if dp[i][j] != INF:
#             new = translate(j,C[i][1:])
#             dp[i+1][new] = min(dp[i+1][new], dp[i][j]+C[i][0])

#         # 実行しない場合
#         dp[i+1][j] = min(dp[i+1][j],dp[i][j])

# # print(*dp, sep="\n")
# if dp[N][(P+1)**K-1] == INF:
#     print(-1)
# else:
#     print(dp[N][(P+1)**K-1])