import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
medicines = [list(map(int,input().split())) for _ in range(N)]

from collections import defaultdict
dict = defaultdict(int)
for a,b in medicines:
    dict[a] += b

medicines = []
for key in dict:
    medicines.append((key,dict[key]))
medicines.sort(key=lambda x:x[0])

# print(medicines)
cur = 0
for a,b in medicines:
    cur += b

day = 1
for i in range(N):
    # print(day,cur)
    if cur <= K:
        print(day)
        exit()
    day = medicines[i][0]+1
    cur -= medicines[i][1]
print(day)