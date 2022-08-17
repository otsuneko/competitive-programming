N = int(input())
X = list(map(int,input().split()))

d1 = d2 = d3 = 0
for x in X:
    d1 += abs(x)
    d2 += x**2
    d3 = max(d3,abs(x))
print(d1)
print(d2**0.5)
print(d3)