N = int(input())
A = list(map(int,input().split()))

from collections import deque
q=deque()
cur = A.count(1)
ans = set([cur])
for c in A:
    q.append(c)  ## dequeの右端に要素を一つ追加する。
    if c == 0:
        cur += 1
    else:
        cur -= 1
    ans.add(cur)

    while q and q[0] == 0:
        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く
        if rm == 0:
            cur -= 1
        else:
            cur += 1
        ans.add(cur)

print(len(ans))