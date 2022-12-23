from collections import Counter

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

N = int(input())
table = prime_decomposition(N)
count = Counter(table)

ans = 0
for c in count:
    n = count[c]
    sub = 1
    while n-sub >= 0:
        ans += 1
        n -= sub
        sub += 1
print(ans)