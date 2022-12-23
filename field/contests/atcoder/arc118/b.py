from collections import Counter
# from sys import stdin
# input = lambda:stdin.readline().rstrip()
# stdin = open('tmp\\arc118_b\\sample-5.in')

K,N,M = map(int,input().split())
A = list(map(int,input().split()))

B = []
for i in range(K):
    B.append(M*A[i]//N)

total = 0
diff = []
for i in range(K):
    total += B[i]
    diff.append(N*B[i] - M*A[i])

sort_diff = sorted(diff)
remain = M - total

check = Counter(sort_diff[:remain])
for i in range(K):
    if remain > 0 and check[diff[i]] > 0:
        check[diff[i]] -= 1
        B[i] += 1
        remain -= 1

print(*B)
