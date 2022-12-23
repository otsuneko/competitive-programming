def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

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

A,B = map(int,input().split())

n = gcd(A,B)
p = set(prime_decomposition(n))
print(len(p)+1)