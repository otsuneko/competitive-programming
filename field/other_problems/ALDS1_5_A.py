# import itertools
# n = int(input())
# A = list(map(int,input().split()))
# q = int(input())
# m = list(map(int,input().split()))

# check = set(m)
# flag = [False]*q
# bit_list = list(itertools.product([0, 1], repeat=n))
# for b in bit_list:
#     total = 0
#     for i in range(n):
#         if b[i] == 1:
#             total += A[i]
#     if total in check:
#         for i in range(q):
#             if total == m[i]:
#                 flag[i] = True

# for f in flag:
#     if f:
#         print("yes")
#     else:
#         print("no")

#https://judge.u-aizu.ac.jp/onlinejudge/review.jsp?rid=2472062#1
n = int(input())
*A, = map(int, input().split())
q = int(input())
*Q, = map(int, input().split())

bit = 1
print(bit, bin(bit))
for a in A:
    bit |= bit << a
    print(bit, bin(bit))

for q in Q:
    print("yes"*((bit >> q) & 1)or"no")

'''sample
5
1 5 7 10 21
4
2 4 17 8

'''