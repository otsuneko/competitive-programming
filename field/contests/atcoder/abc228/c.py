import bisect
'''
bisect.bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect.bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す
bisect.bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)
'''

N,K = map(int,input().split())
score = []
score_order = []
for i in range(N):
    tmp = list(map(int,input().split()))
    score_order.append((sum(tmp),i))
    score.append(sum(tmp))
score_order.sort()
score.sort()

ans = [False]*N
for i in range(N):
    new_score = score_order[i][0]+300
    rank = bisect.bisect(score,new_score)
    if N-rank < K:
        ans[score_order[i][1]] = True

for a in ans:
    print(["No","Yes"][a])