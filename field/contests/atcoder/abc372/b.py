import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

M = int(input())

ans = []
while M > 0:
    if M%3 != 0:
        ans.append(0)
        M -= 1
        continue
    a = 0
    while 1:
        if 3**a > M:
            ans.append(a-1)
            M -= 3**(a-1)
            break
        a += 1

print(len(ans))
print(*ans)
