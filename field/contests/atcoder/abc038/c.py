from collections import deque

N = int(input())
A = list(map(int,input().split()))

ans = 0
ma = 0
q=deque()
for c in A:
    q.append(c)  ## dequeの右端に要素を一つ追加する。
    ma = max(ma,c)

    while not :
        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く

    ans += 1
print(ans)