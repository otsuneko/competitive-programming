N = list(input())

d = 0
for n in N:
    d += int(n)

print(["No","Yes"][d%9 == 0])
