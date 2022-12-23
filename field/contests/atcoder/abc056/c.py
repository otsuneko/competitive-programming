X = int(input())

s = 0
cnt = 0
ans = 10**18
while s < X:
    cnt += 1
    if X - s > 2*cnt+1:
        s += cnt
    elif X - s == 2*cnt+1:
        ans = cnt+1
        break
    else:
        ans = cnt + X-s-cnt
        break

print(ans)