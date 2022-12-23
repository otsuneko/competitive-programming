N = int(input())
A = list(map(int,input().split()))

l = min(8,N)
check = [[] for i in range(200)]
for bit in range(1<<N):
    total = 0
    cmb = []
    for i in range(N):
        if bit & (1<<i):
            total += A[i]
            cmb.append(i+1)
    if total:
        total %= 200
        check[total].append(cmb)
        if len(check[total]) == 2:
            print("Yes")
            print(len(check[total][0]),*check[total][0])
            print(len(check[total][1]),*check[total][1])
            break
else:
    print("No")

# original code(WA)
# import sys
# sys.setrecursionlimit(10**7)
# def dfs(i,num_list,s):
#     if i == N:
#         #  or tuple(num_list) in check[s%200]:
#         return
#     check[s%200].add(tuple(num_list))
#     dfs(i+1,num_list[:],s)
#     num_list.append(i)
#     dfs(i+1,num_list[:],(s+A[i])%200)

# N = int(input())
# A = list(map(int,input().split()))

# if N == 2:
#     if abs(A[0]-A[1])%200 == 0:
#         print("Yes")
#         print("1 1")
#         print("1 2")
#     else:
#         print("No")
#     exit()

# for i in range(N):
#     A[i] = A[i]%200

# check = [set([]) for i in range(201)]
# num_list = []
# s = 0
# dfs(0,num_list,s)
# print(check)

# for s in check:
#     if len(s) > 1:
#         flag = True
#         for i in range(len(s)):
#             print(s[0][i],s[1][i])
#             if s[0][i] == s[1][i]:
#                 flag = False
#                 break
#         if flag:
#             print("Yes")
#             ans = [[] for i in range(2)]
#             idx = 0
#             for a in s:
#                 if idx == 2:
#                     break
#                 for n in a:
#                     ans[idx].append(n+1)
#                 idx += 1
#             print(len(ans[0]),*ans[0])
#             print(len(ans[1]),*ans[1])
#             break
# else:
#     print("No")