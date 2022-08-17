from collections import deque,Counter
N,K = map(int,input().split())
a = list(map(int,input().split()))
q=deque()

ans = 0
counter = Counter()
cnt = 0
for c in a:
    q.append(c)  ## dequeの右端に要素を一つ追加する。
    if counter[c] == 0:
        cnt += 1
    counter[c] += 1
    while not cnt <= K:
        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く
        if counter[rm] == 1:
            cnt -= 1
        counter[rm] -= 1            

    ans = max(ans,len(q))
print(ans)