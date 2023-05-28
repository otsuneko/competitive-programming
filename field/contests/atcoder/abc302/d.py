N,M,D = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

C = []

for a in A:
    C.append((a,0))
for b in B:
    C.append((b,1))
C.sort()

ans = -1
curA = curB = 0
for val,who in C:
    if who == 0:
        curA = val
        if curB != 0 and abs(curA - curB) <= D:
            ans = max(ans,curA + curB)
    else:
        curB = val
        if curA != 0 and abs(curA - curB) <= D:
            ans = max(ans,curA + curB)
print(ans)