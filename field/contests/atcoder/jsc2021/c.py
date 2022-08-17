A,B = map(int, input().split())

ans = 1
for i in range(2,B+1):
    cnt = 0
    for j in range(i,B+1,i):
        if A <= j <= B:
            cnt += 1
            if cnt == 2:
                ans = max(ans, i)
print(ans)

# original answer
# A,B = map(int, input().split())
 
# ans = 1
# for i in reversed(range(1,B+1)):
#     cnt = 0
#     mul = 1
#     while i*mul <= B:
#         if A <= i*mul <= B:
#             cnt += 1
#         mul += 1
#     if cnt > 1:
#         ans = i
#         break
 
# print(ans)