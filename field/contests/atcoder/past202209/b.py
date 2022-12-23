N = list(input())

for _ in range(2):
    N.pop()
    if not N:
        print(0)
        exit()
print("".join(N))