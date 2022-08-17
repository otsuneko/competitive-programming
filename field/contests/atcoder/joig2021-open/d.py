from operator import itemgetter
N,M,D = map(int,input().split())
pict = [tuple(map(int,input().split())) for _ in range(N)]
pict_dist = sorted(pict)
pict_score = sorted(pict,key=itemgetter(1))

left = 0
right = N-1
mid = (left+right)//2
ans = pict_score[mid]
prev = -1

while 1:

    flag = False
    pic_n = N-mid
    if pic_n < M:
        flag = False
    else:
        
    for 
# import sys
# sys.setrecursionlimit(10**7)
# def dfs(i, x, score, remain):
#     print(i,x,score,remain)
#     if i == N:
#         if remain == 0:
#             return score
#         else:
#             return float("INF")
    
#     if pict[i][0] - x >= D:
#         score1 = dfs(i+1, pict[i][0], min(score,pict[i][1]), remain-1)
#         score2 = dfs(i+1, x, score, remain)
#         if score1 != float("INF") and score2 != float("INF"):
#             return min(score1,score2)
#         elif score1 == float("INF"):
#             return score2
#         elif score2 == float("INF"):
#             return score1
#         else:
#             return float("INF")
#     else:
#         return dfs(i+1, x, score, remain)

# N,M,D = map(int,input().split())
# pict = [tuple(map(int,input().split())) for _ in range(N)]
# pict.sort()

# ans = dfs(0,-float("INF"),float("INF"),M)

# if ans == float("INF"):
#     print(-1)
# else:
#     print(ans)