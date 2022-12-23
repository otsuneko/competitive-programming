dishes = [int(input()) for _ in range(5)]

import itertools

seq = (0,1,2,3,4)
ptr = list(itertools.permutations(seq)) #順列列挙 5P3

ans = 10**18
for p in ptr:
    t = 0
    for i in range(5):
        t += dishes[p[i]]
        if i < 4 and t%10:
            t += 10-t%10
    ans = min(ans,t)
print(ans)