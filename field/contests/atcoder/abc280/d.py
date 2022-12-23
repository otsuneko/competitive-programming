def prime_decomposition(n):
    i = 2
    table = []
    while i * i <= n:
      while n % i == 0:
        n = n//i
        table.append(i)
      i += 1
    if n > 1:
      table.append(n)
    return table

K = int(input())

from collections import Counter
prime_K = prime_decomposition(K)
count = Counter(prime_K)

ans = 0
for p in count:
    cnt = 0
    for i in range(1,count[p]+1):
        cand = p*i
        while cand%p == 0:
            cand //= p
            cnt += 1
        if cnt >= count[p]:
            ans = max(ans, p*i)
            break
print(ans)