N = int(input())
S = list(map(int,input().split()))

possible_area = set()
for a in range(1,1000):
    for b in range(1,1000):
        s = 4*a*b + 3*a + 3*b
        if s <= 1000:
            possible_area.add(s)

cor_n = 0
for s in S:
    if s in possible_area:
        cor_n += 1
print(N-cor_n)