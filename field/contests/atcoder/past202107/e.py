N = int(input())

table = []
for i in range(1,31):
    X = (3**i + 1) * (3**(30-i))
    table.append(X)

if N in table:
    print(table.index(N)+1)
else:
    print(-1)