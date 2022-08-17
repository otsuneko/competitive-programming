from collections import deque
N = int(input())
S = []
for _ in range(N):
    s = list(input())
    s.sort()
    S.append("".join(s))
print(S)
q=deque()
ans = ""
for c in S[0]:
    q.append(c)  ## dequeの右端に要素を一つ追加する。

    flg = True
    for i in range(1,N):
        s = "".join(q)
        if s not in S[i]:
            flg = False
            break
    if flg and len(q) > len(ans):
        ans = s

    while not flg:
        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く
        flg = True

print("".join(ans))