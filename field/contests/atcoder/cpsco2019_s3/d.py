from collections import deque
'''
上書き操作は終了状態から逆順に見る(https://atcoder.jp/contests/abc329/tasks/abc329_e)
check関数では、あるidxに対する逆順の操作が可能かを確認する
可能な場合はそのidxを処理済に更新し、queに対して次に確認すべきidxを追加する
'''
def check(idx):
    '''
    そのidxが既に操作済みの場合はreturn
    '''
    if done[idx]:
        return

    '''
    そのidxに対する逆順の操作が可能かチェック(問題によってチェック内容を変える)
    可能な場合はそのidxに処理済フラグを立て、その操作で次に実行可能となるidxをqueに追加
    '''
    flg = True
    for i in range(3):
        flg &= (S[idx+i] == "#" or S[idx+i]==T[i])
    
    if flg:
        done[idx] = True
        S[idx:idx+M] = ["#"]*M
        for idx2 in range(max(0,idx-M+1),min(N-M+1,idx+M)):
            que.append(idx2)

N = int(input())
M = 3
S = list(input())
T = ["R","G","B"]

que = deque()
done = [False]*N

'''
終了状態で逆順操作可能なidxを処理し、次に操作すべきidxをqueに追加
'''
for idx in range(N-M+1):
    check(idx)

'''
queが空になるまでチェックを繰り返し、最終的に初期状態まで戻せるか判定
'''
while que:
    idx = que.popleft()
    check(idx)

print(["No","Yes"][S == ["#"]*N])