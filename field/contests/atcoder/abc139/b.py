A,B = map(int,input().split())
print(((B-1)+(A-1)-1)//(A-1))

# n = 1
# limit = 1
# cur = 0
# ans = 0
# while n < B:
#     if cur < limit:
#         ans += 1
#         cur += 1
#         n += A-1
#     else:
#         cur = 0
#         limit *= A
# print(ans)