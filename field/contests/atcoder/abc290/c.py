N,K = map(int,input().split())
A = list(map(int,input().split()))
A = list(set(sorted(A)))
A.sort()

cur = 0
cnt = 0
for a in A:
    if a == cur:
        cur += 1
        cnt += 1
        if cnt == K:
            break
    else:
        break
print(cur)