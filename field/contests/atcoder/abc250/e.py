N =int(input())
A =list(map(int,input().split()))
B =list(map(int,input().split()))
Q =int(input())

# Zobrist Hash
import random

rand = {}
for a,b in zip(A,B):
    if a not in rand:
        rand[a] = random.randrange(1 << 64)

    if b not in rand:
        rand[b] = random.randrange(1 << 64)

zhA,zhB = [0],[0]
setA,setB = set(),set()
for a,b in zip(A,B):
    if a in setA:
        zhA.append(zhA[-1])
    else:
        zhA.append(zhA[-1] ^ rand[a])
        setA.add(a)

    if b in setB:
        zhB.append(zhB[-1])
    else:
        zhB.append(zhB[-1] ^ rand[b])
        setB.add(b)

for _ in range(Q):
    x,y = map(int, input().split())
    if zhA[x] == zhB[y]:
        print("Yes")
    else:
        print("No")

# hamamu-san
# from collections import defaultdict
# dict = defaultdict(int)

# cnt = 1
# for a in A:
#     if dict[a] == 0:
#         dict[a] = cnt
#         cnt += 1

# for b in B:
#     if dict[b] == 0:
#         dict[b] = cnt
#         cnt += 1

# sA = set()
# sB = set()
# cnt_setA = [0]*N
# cnt_setB = [0]*N
# maA = [0]*N
# maB = [0]*N
# for i in range(N):
#     sA.add(dict[A[i]])
#     sB.add(dict[B[i]])
#     cnt_setA[i] = len(sA)
#     cnt_setB[i] = len(sB)
#     maA[i] = max(dict[A[i]],maA[i-1])
#     maB[i] = max(dict[B[i]],maB[i-1])

# for _ in range(Q):
#     x,y =map(int,input().split())
#     x,y = x-1,y-1
#     if cnt_setA[x] == cnt_setB[y] and maA[x] == maB[y]:
#         print("Yes")
#     else:
#         print("No")