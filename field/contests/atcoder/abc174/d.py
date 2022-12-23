N = int(input())
C = list(input())

ans = 0
l = 0
r = N-1
while 1:
    if l > r:
        break
    if C[l] == "W":
        if C[r] == "R":
            ans += 1
            l += 1
            r -= 1
        else:
            r -= 1
    else:
        l += 1
print(ans)