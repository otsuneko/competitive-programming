n = 100
l = [i**2 for i in range(1,n)]
import itertools
cmb = itertools.combinations(l,4)

ans = set([])
for i in range(1,10):
    cnt = 0
    for c in cmb:
        print(c)
        cnt += 1
        if cnt == 10:
            break
        tmp = []
        for a in c:
            tmp.append(a%i)
        print(tmp)
        for t in tmp:
            if tmp.count(t) == 2:
                ans.add(i)
                break
print(ans)