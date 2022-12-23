def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

def gcdlist(l):
    a = l[0]
    for i in range(len(l)):
        a = gcd(a,l[i])
    return a

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
A = list(map(int,input().split()))

GCD = gcdlist(A)

ans = 0
for a in A:
    if a == GCD:
        continue
    mul = a//GCD
    prime = prime_decomposition(mul)
    if set(prime) not in [{2},{3},{2,3}]:
        print(-1)
        exit()
    ans += len(prime)

print(ans)