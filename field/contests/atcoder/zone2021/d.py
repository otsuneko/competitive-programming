S = input()
from collections import deque
T = deque()

flg = False
for s in S:
    if s == "R":
        flg = not flg
    else:
        if flg:
            if T and T[0] == s:
                T.popleft()
            else:
                T.appendleft(s)
        else:
            if T and T[-1] == s:
                T.pop()
            else:
                T.append(s)

if flg:
    print("".join(T)[::-1])
else:
    print("".join(T))
