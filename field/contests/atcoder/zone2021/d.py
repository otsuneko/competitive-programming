from collections import deque
S = list(input())

T = deque([])
flag = False
for s in S:
    if s == "R":
        flag = not flag
    else:
        if flag:
            if T and T[0] == s:
                T.popleft()
                continue
            else:
                T.appendleft(s)        
        else:
            if T and T[len(T)-1] == s:
                T.pop()
                continue
            else:
                T.append(s)

T = list(T)
if flag:
    T = T[::-1]

print("".join(T))