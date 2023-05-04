# S = list(input())

# from collections import defaultdict
# dict = defaultdict(int)

# dig_cnt = ["0"]*10
# dict["".join(dig_cnt)] += 1
# for s in S:
#     d = int(s)
#     dig_cnt[d] = "1" if dig_cnt[d] == "0" else "0"
#     dict["".join(dig_cnt)] += 1

# def nCr(n, r):

#     res = 1
#     for i in range(r):
#         res = (res*(n-i))//(i+1)

#     return res

# ans = 0
# for key in dict:
#     ans += nCr(dict[key],2)
# print(ans)


# Zobrist Hash(例題：ABC250 - E - Prefix Equality)
import random

S = list(input())

# Sの各要素をユニークな乱数に変換
rand = {}
for s in S:
    if s not in rand:
        rand[s] = random.randrange(1 << 64)

# リストの先頭から順に集合の状態をハッシュ化(累積XOR)
zhA = [0]
for s in S:
    zhA.append(zhA[-1] ^ rand[s])

ans = 0
from collections import defaultdict
dict = defaultdict(int)
for zh in zhA:
    if dict[zh]:
        ans += dict[zh]
    dict[zh] += 1
print(ans)