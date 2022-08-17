def is_prime(n):
    for i in range(2, n + 1):
        if i * i > n:
            break
        if n % i == 0:
            return False
    return n != 1

vendor = [list(map(int,input().split())) for _ in range(20)]

ans = 0
for i in range(20):
    for j in range(20):
        if is_prime(vendor[i][j]):
            ans += 1

print(ans)