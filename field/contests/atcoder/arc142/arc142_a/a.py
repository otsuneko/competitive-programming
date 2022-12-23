N,K = map(int,input().split())

s = str(K)
li = set()
zero = "0"
cnt = 0
while 1:
    if len(s+zero*cnt) <= 13:
        li.add(s+zero*cnt)
        if s[-1] != "0":
            li.add(s[::-1]+zero*cnt)
    else:
        break
    cnt += 1

li = sorted(list(li))
ans = set()
for l in li:
    x = int(l)
    if x > N:
        continue
    if l[-1] == "0":
        if x == K:
            ans.add(x)
    inv_x = int(l[::-1])
    inv_x2 = int(str(inv_x)[::-1])
    if inv_x > N or inv_x2 > N:
        continue
    if min(x,inv_x,inv_x2) == K:
        print(x,inv_x,inv_x2)
        ans.add(l)

print(len(ans))