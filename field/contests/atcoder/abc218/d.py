from collections import defaultdict
N = int(input())
dic_x = defaultdict(list)
dic_y = defaultdict(set)

for _ in range(N):
    x,y = map(int,input().split())
    dic_x[x].append((x,y))
    dic_y[y].add((x,y))

for x in dic_x:
    dic_x[x].sort(key=lambda x:(x[0],x[1]))

ans = set()
for x in dic_x:
    for i in range(len(dic_x[x])):
        x1,y1 = dic_x[x][i]
        for j in range(i+1,len(dic_x[x])):
            x2,y2 = dic_x[x][j]
            for x3,y3 in dic_y[y1]:
                if x1 != x3 and (x3,y2) in dic_y[y2]:
                    ans.add((min(x1,x2,x3), min(y1,y2,y3), max(x1,x2,x3), max(y1,y2,y3)))
print(len(ans))