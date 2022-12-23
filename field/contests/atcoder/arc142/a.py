N,K = map(int,input().split())

s = str(K)
li = set()
zero = "0"
cnt = 0
while 1:
    if len(s+zero*cnt) <= 13:
        li.add(s+zero*cnt)
        li.add(s[::-1]+zero*cnt)
    else:
        break
    cnt += 1

li = sorted(list(li))
ans = 0
for l in li:
    x = int(l)
    if x > N:
        continue
    inv_x = int(l[::-1])
    inv_x2 = int(str(inv_x)[::-1])
    if min(x,inv_x,inv_x2) == K:
        # print(x,inv_x,inv_x2)
        ans += 1

print(ans)