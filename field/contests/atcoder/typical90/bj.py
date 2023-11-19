import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18


from collections import deque
'''
上書き操作は終了状態から逆順に見る
check関数では、あるidxに対する逆順の操作が可能かを確認する
可能な場合はqueに対して次に確認すべきidxを追加する
'''
def check(idx):
    global cnt
    '''
    そのidxが既に操作済みの場合はreturn
    '''
    if balls[idx] == "W":
        return

    '''
    そのidxに対する逆順の操作が可能かチェックする
    可能な場合はそのidxに処理済みフラグを立て、その操作によって
    次に実行可能となるidxをqueに追加する
    問題によって確認ロジックは異なる
    '''
    a,b = items[idx]
    a,b = a-1,b-1

    # 自分がWならBにできる場合は優先的にそうする
    if idx in [a,b]:
        balls[idx] = "W"
        ans.append(idx)
        for nidx in nxt[idx]:
            if balls[nidx] == "B":
                que.append(nidx)
    elif not (balls[a] == "B" and balls[b] == "B"):
        balls[idx] = "W"
        ans.append(idx)
        for nidx in nxt[idx]:
            if balls[nidx] == "B":
                que.append(nidx)

N = int(input())
items = [list(map(int,input().split())) for _ in range(N)]
balls = ["B"]*N
ans = []
que = deque()
nxt = [set() for _ in range(N)]

for i in range(N):
    a,b = items[i]
    a,b = a-1,b-1
    nxt[a].add(i)
    nxt[b].add(i)


for i in range(N):
    check(i)

while que:
    idx = que.popleft()
    check(idx)

ans = ans[::-1]
if len(ans) != N:
    print(-1)
else:
    for a in ans:
        print(a+1)