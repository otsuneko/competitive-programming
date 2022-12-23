N,X =map(int,input().split())
S = list(input())

cur_depth = 0
tmp = X
while tmp > 0:
    tmp //= 2
    cur_depth += 1
cur_depth -= 1

tmp = X
for s in S:
    if s == "U":
        if cur_depth < 60:
            X //= 2
        elif cur_depth == 60:
            ans = tmp
        cur_depth -= 1
    elif s == "L":
        if cur_depth < 59:
            X *= 2
        elif cur_depth == 59:
            tmp = X
        else:
            pass
        cur_depth += 1
    elif s == "R":
        if cur_depth < 59:
            X = X*2+1
        elif cur_depth == 59:
            tmp = X
        else:
            pass
        cur_depth += 1
    # print(X,cur_depth)

print(X)