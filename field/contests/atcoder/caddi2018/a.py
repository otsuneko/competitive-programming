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

from collections import Counter
N,P = map(int,input().split())

prime = prime_decomposition(P)
count = Counter(prime)
ans = 1
for key in count:
    if count[key] >= N:
        ans *= key ** (count[key]//N) 
print(ans)