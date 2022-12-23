N,X = map(int,input().split())
A = list(map(int,input().split()))

known = [False]*N
known[X-1] = True

cur = X-1
while 1:
    if known[A[cur]-1] == False:
        known[A[cur]-1] = True
        cur = A[cur]-1
    else:
        break
print(known.count(True))