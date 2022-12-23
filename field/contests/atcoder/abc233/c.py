from collections import defaultdict

N,X =map(int,input().split())
dict = defaultdict(int)
dict[X] = 1
for i in range(N):
    que =list(map(int,input().split()))
    A = que[1:]

    dict2 = defaultdict(int)
    for key in dict:
        for a in A:
            if key%a == 0:
                dict2[key//a] += dict[key]
    
    dict = dict2

if 1 in dict:
    print(dict[1])
else:
    print(0)
