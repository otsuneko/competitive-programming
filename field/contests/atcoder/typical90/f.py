import heapq  # heapqライブラリのimport

# 0-indexed
def int_to_lower(k):
    return chr(k+97)

def lower_to_int(c):
    return ord(c)-97

N,K =map(int,input().split())
S = input()

### 解法1 ###
ans = []
hq = []
idx = 0
for i,c in enumerate(S):
    heapq.heappush(hq,(lower_to_int(c),i))

    if i >= N-K:
        while hq:
            d,j = heapq.heappop(hq)
            if idx <= j:
                ans.append(int_to_lower(d))
                idx = j+1
                break
print("".join(ans))

### 解法2 ###
# #chr_idx[c][n]:j文字目の文字より右側にある文字iのうち、最も左側にある文字のインデックス
# chr_idx = [[10**9]*N for _ in range(26)]

# for n in range(N-1,-1,-1):
#     if n == N-1:
#         chr_idx[lower_to_int(S[n])][n] = n
#     else:
#         for c in range(26):
#             if lower_to_int(S[n]) == c:
#                 chr_idx[lower_to_int(S[n])][n] = n
#             else:
#                 chr_idx[c][n] = chr_idx[c][n+1]

# ans = []
# idx = 0
# for k in range(K):
#     for c in range(26):
#         if chr_idx[c][idx] <= N-(K-k):
#             ans.append(int_to_lower(c))
#             idx = chr_idx[c][idx]+1
#             break

# print("".join(ans))