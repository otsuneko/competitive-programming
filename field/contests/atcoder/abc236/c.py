N,M = map(int,input().split())
S = list(map(str,input().split()))
T =list(map(str,input().split()))
check = set(T)

for s in S:
    if s in check:
        print("Yes")
    else:
        print("No")