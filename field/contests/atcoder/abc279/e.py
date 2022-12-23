# 上下からの累積和
N,M = map(int,input().split())
A = list(map(int,input().split()))

# 上からの累積和で、各回における1の場所を覚えておく。
cumsum_top = [0]
B = [i for i in range(1,N+1)]
for a in A[:M-1]:
    s,t = B[a-1],B[a]
    B[a-1],B[a] = B[a],B[a-1]
    if s == 1:
        cumsum_top.append(a)
    elif t == 1:
        cumsum_top.append(a-1)
    else:
        cumsum_top.append(cumsum_top[-1])

# print(cumsum_top)

# 下からの累積和で、ある回をスキップした場合の1の場所を求める。
B = [i for i in range(1,N+1)]
cumsum_bottom = [cumsum_top[-1]+1]
for i,a in enumerate(A[::-1][:M-1]):
    s,t = B[a-1],B[a]
    B[a-1],B[a] = B[a],B[a-1]
    cumsum_bottom.append(B[cumsum_top[M-2-i]])

for ans in cumsum_bottom[::-1]:
    print(ans)
    
# 各回で入れ替わった要素を記録しておく。
# i回目の入れ替えをしなかったBは、全て入れ替えた場合のBに対して
# i回目の入れ替え対象番号を入れ替えることで求められる。
# from collections import defaultdict

# N,M = map(int,input().split())
# A = list(map(int,input().split()))

# exchanges = []
# B = [i for i in range(1,N+1)]

# for a in A:
#     B[a-1],B[a] = B[a],B[a-1]
#     exchanges.append((B[a-1],B[a]))

# dict = defaultdict(int)
# for idx,b in enumerate(B):
#     dict[b] = idx

# for i,(a,b) in enumerate(exchanges):

#     if a == 1:
#         print(dict[b]+1)
#     elif b == 1:
#         print(dict[a]+1)
#     else:
#         print(dict[1]+1)