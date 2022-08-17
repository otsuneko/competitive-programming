N,K =map(int,input().split())

cnt = 0
# Kが1個
cnt += (K-1) * (N-K) * 6

# Kが2個
cnt += 3 * (N-1)

# Kが3個
cnt += 1

print(cnt/(N**3))