N = int(input())
dish = list(map(int,input().split()))

mat = [[0]*2*(10**5) for _ in range(2*(10**5))]
ans = 0
seen = set()

# for r in ridx:
#     if r-1 not in seen:    
#         tmp = 0
#         for i in range(N):
#             if i in [dish[(i-1+r-1)%N],dish[(i+r-1)%N],dish[(i+1+r-1)%N]]:
#                 tmp += 1
#         ans = max(ans,tmp)
#         seen.add(r-1)

#     if r not in seen:    
#         tmp = 0
#         for i in range(N):
#             if i in [dish[(i-1+r)%N],dish[(i+r)%N],dish[(i+1+r)%N]]:
#                 tmp += 1
#         ans = max(ans,tmp)
#         seen.add(r)

#     if r+1 not in seen:    
#         tmp = 0
#         for i in range(N):
#             if i in [dish[(i-1+r+1)%N],dish[(i+r+1)%N],dish[(i+1+r+1)%N]]:
#                 tmp += 1
#         ans = max(ans,tmp)
#         seen.add(r+1)

# print(ans)