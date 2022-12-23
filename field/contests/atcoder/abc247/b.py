N =int(input())

name = []
for _ in range(N):
    s,t =map(str,input().split())
    name.append([s,t])

for i in range(N):
    flg = False
    for adana in name[i]:
        adana_ok = True
        for j in range(N):
            if i == j:
                continue
            if (adana in name[j]):
                adana_ok = False
    if adana_ok == True:
        flg = True
        
    if not flg:
        print("No")
        exit()

print("Yes")

# from collections import defaultdict
# dict = defaultdict(int)
# name = []
# for _ in range(N):
#     s,t =map(str,input().split())
#     dict[s] += 1
#     dict[t] += 1
#     name.append([s,t])

# ans = "Yes"
# for s,t in name:
#     if s != t and not (dict[s] == 1 or dict[t] == 1):
#         ans = "No"
#         break
# print(ans)
