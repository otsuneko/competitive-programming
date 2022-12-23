from collections import deque
N = int(input())
A = input.split()

b = "".join(A)
n = len(b)
b = int(b,2)
bit1 = (1<<n)-1
bit10 = 1<<n-1

while 1:

    if not b & bit1:
        print("Yes")
        exit()

    while not b & 1:
        b = b >> 1
        bit1 = bit1 >> 1
        bit10 = bit10 >> 1
        n -= 1

    b = b ^ bit1 # NOT(負数考慮なしの01反転)
    if b & bit10:
        b &= ~bit10 # 最上位の1を0に
        bit1 = bit1 >> 1
        bit10 = bit10 >> 1
        n -= 1
    else:
        print("No")
        exit()

# flg = False
# while 1:
#     while len(A) and (A[-1] ^ flg) == 0:
#         A.pop()
#     if len(A):
#         if (A[0] ^ flg) == 0:
#             flg = not flg
#             A.popleft()
#         else:
#             print("No")
#             exit()
#     else:
#         print("Yes")
#         exit()
