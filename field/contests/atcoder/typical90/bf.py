N,K = map(int,input().split())

su = [0]*10**5
for i in range(10**5):
    su[i] = sum(map(int, list(str(i))))

x = N
li = [N]
check = set([N])
for k in range(K):
    x = (x + su[x])%(10**5)
    if x not in check:
        li.append(x)
        check.add(x)
    else:
        break

if K <= len(li):
    print(x)
else:
    idx = li.index(x)
    loop = len(li)-idx
    print(li[idx + (K-idx)%loop])