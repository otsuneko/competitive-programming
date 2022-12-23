from collections import deque
S = deque(input())
Q = int(input())

flag = False
for _ in range(Q):
    query = list(map(str,input().split()))

    if query[0] == "1":
        flag = not flag
    else:
        F = int(query[1])
        C = query[2]

        if flag:
            if F == 1:
                S.append(C)
            else:
                S.appendleft(C)
        else:
            if F == 1:
                S.appendleft(C)
            else:
                S.append(C)

if flag:
    print("".join(list(S)[::-1]))
else:
    print("".join(S))