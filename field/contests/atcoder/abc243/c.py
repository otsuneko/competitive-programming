from collections import defaultdict
dict = defaultdict(list)

N =int(input())
for i in range(N):
    x,y =map(int,input().split())
    dict[y].append((x,i))
S = list(input())


for key in dict:
    li = sorted(dict[key])
    l,r = 0,len(li)-1
    
    while l < r:
        if S[li[l][1]] == "L":
            l += 1
        elif S[li[r][1]] == "R":
            r -= 1
        else:
            if li[l][0] < li[r][0]:
                print("Yes")
                exit()
print("No")