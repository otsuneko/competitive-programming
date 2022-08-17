# # ランレングス圧縮解法
# import bisect
# # 順序付きSet(insertの使い分けによって重複有り/無しの使い分け可能)
# class MultiSet:
#     def __init__(self):
#         self.total = 0 # Multi_setに含まれる要素数
#         self.ms = dict() # 各要素の個数カウント用
#         self.lr = [] # 要素の重複を排除した昇順リスト(一度追加されたものはdelete処理の後も残る)

#     # 重複を許さない挿入
#     def insert_unique(self, x):
#         if x in self.ms:
#             if self.ms[x] == 0:
#                 self.ms[x] = 1
#                 self.total += 1
#         else:
#             self.total += 1
#             self.ms[x] = 1
#             bisect.insort(self.lr, x)

#     # 重複を許す挿入
#     def insert_multi(self, x):
#         self.total += 1
#         if x in self.ms:
#             self.ms[x] += 1
#         else:
#             self.ms[x] = 1
#             bisect.insort(self.lr, x)

#     # 要素の存在判定(有り:1、無し:0をReturn)
#     def find(self, x):
#         return self.ms.get(x, 0)

#     # 要素の削除(重複を許している場合は値がxの要素を全て削除)
#     def delete(self, x):
#         if x in self.ms:
#             self.total -= self.ms[x]
#             self.ms[x] = 0

#     # 値がl以上r以下の要素を抽出したリストをReturn
#     def dump(self, l, r):
#         lb = bisect.bisect_left(self.lr, l)
#         ub = bisect.bisect_right(self.lr, r)
#         res = []
#         for i in range(lb, ub):
#             k = self.lr[i]
#             v = self.ms[k]
#             res += [k]*v
#         return res

# S = list(input())
# N = len(S)

# div = MultiSet()
# div.insert_unique(0)
# ans = [0]*N
# i = j = 0
# while i < N:
#     j = i
#     while j < N and S[j] == S[i]:
#         j += 1
#     div.insert_unique(j)

#     if S[i] == "L":
#         num_R = div.lr[div.total-2] - div.lr[div.total-3]
#         num_L = div.lr[div.total-1] - div.lr[div.total-2]
#         ans[i-1] = (num_R+1)//2 + num_L//2
#         ans[i] = num_R//2 + (num_L+1)//2
#     i = j
# print(*ans)

# ダブリング解法
S = list(input())
N = len(S)

dp = [[0]*N for _ in range(21)]

for i in range(N):
    if S[i] == "R":
        dp[0][i] = i+1
    else:
        dp[0][i] = i-1
    
for p in range(20):
    for i in range(N):
        dp[p+1][i] = dp[p][dp[p][i]]

# print(*dp, sep="\n")

ans = [0]*N
for i in range(N):
    ans[dp[20][i]] += 1

print(*ans)