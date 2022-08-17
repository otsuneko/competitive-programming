S,T = map(int,input().split())

ans = 0
for a in range(S+1):
    for b in range(S+1-a):
        for c in range(S+1-a-b):
            if a*b*c <= T:
                ans += 1
            else:
                break
print(ans)

# ans = 0
# for a in range(101):
#     for b in range(101):
#         for c in range(101):
#             if a+b+c <= S and a*b*c <= T:
#                 ans += 1
# print(ans)