from collections import deque

S = input()
K = int(input())

q=deque()
ans = 0
used_idx = set()
for i,c in enumerate(S):
    if K > 0 or c == "X":
        q.append((i,c))  ## dequeの右端に要素を一つ追加する。
        if c == ".":
            K -= 1
            used_idx.add(i)
    ans = max(ans,len(q))

    while K == 0 and (i+1 < len(S) and S[i+1] != "X") and q:
        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く
        if rm[0] in used_idx:
            used_idx.remove(rm[0])
            K += 1

print(ans)