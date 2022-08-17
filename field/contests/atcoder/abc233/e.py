X =list(input())

l = len(X)
s = 0
for x in X:
    s += int(x)
c = 0

###別解###
print((10*int("".join(X))-s)//9)
exit()

ans = []
for i in range(l):
    c += s
    ans.append(str(c%10))
    c //= 10
    s -= int(X[l-i-1])

if c:
    ans.append(str(c%10))

print("".join(ans[::-1]))
