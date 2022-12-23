N = int(input())
ans = [1,0]
for i in range(1,N+1):
    cnt = 0
    n = i
    while n%2 == 0:
        n//= 2
        cnt += 1
    if cnt > ans[1]:
        ans = [i,cnt]
print(ans[0])

# N = int(input())
# pow2 = [2,4,8,16,32,64]

# ans = 1
# for p in pow2:
#     if p > N:
#         break
#     ans = p
# print(ans)