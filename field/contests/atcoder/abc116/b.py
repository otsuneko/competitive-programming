s = int(input())

check = set([s])
m = 1
while 1:
    s = s//2 if s%2==0 else 3*s+1
    m+=1
    if s in check:
        print(m)
        break
    check.add(s)