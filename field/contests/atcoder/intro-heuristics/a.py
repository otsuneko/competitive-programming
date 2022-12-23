import time
import random

# 新たな解の生成
def update_contests(con):
    
    for d in range(D):
        r = random.randint(0,25)
        con[d] = r

# スコア計算
def calc_score(con):

    score = 0
    last = [0]*26

    # 満足度の変化
    for d in range(D):
        score += S[d][con[d]]
        last[con[d]] = d+1

        for t in range(26):
            score -= C[t] * (d+1 - last[t])
            
    return score

# 入力
D =int(input())
C =list(map(int,input().split()))
S =[list(map(int,input().split())) for _ in range(D)]
T =list(map(int,input().split()))
M =int(input())
query =list(map(int,input().split()))

# # 変数
# ans_contests = []
# max_score = 0

# # 初期解生成(乱数)
# contests = []
# for d in range(D):
#     r = random.randint(0,25)
#     contests.append(r)

# start = time.time()

# # 山登り
# while 1:
    
#     # TLE対策
#     now = time.time()
#     if now-start >= 1.75:
#         break

#     # 新たな解の生成
#     update_contests(contests)

#     # スコア計算
#     score = calc_score(contests)

#     # 解の更新
#     if score > max_score:
#         max_score = score
#         ans_contests = contests[:]

# # 解の出力
# for c in ans_contests:
#     print(c+1)