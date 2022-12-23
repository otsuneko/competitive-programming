from collections import defaultdict


d1 = list(map(int,input().split()))
d2 = list(map(int,input().split()))
d3 = list(map(int,input().split()))

prob = defaultdict(int)

for i,p1 in enumerate(d1):
    for j,p2 in enumerate(d2):
        for k,p3 in enumerate(d3):
            prob[i+j+k+3] += p1*p2*p3

for i in range(1,19):
    print(prob[i]/10**6)