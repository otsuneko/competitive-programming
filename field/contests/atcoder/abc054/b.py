import random
N,M =map(int,input().split())
A =[list(input()) for _ in range(N)]
B =[list(input()) for _ in range(M)]

rand = 0
for y in range(M):
    for x in range(M):


# for y1 in range(N-M+1):
#     for x1 in range(N-M+1):
#         for y2 in range(M):
#             for x2 in range(M):
#                 if A[y1+y2][x1+x2] != B[y2][x2]:
#                     break
#             else:
#                 continue
#             break
#         else:
#             print("Yes")
#             exit()
# print("No")