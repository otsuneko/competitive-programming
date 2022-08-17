N =int(input())

s = [1]

for i in range(2,N+1):
    s = s + [i] + s

print(*s)