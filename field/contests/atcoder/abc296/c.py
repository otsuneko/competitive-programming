N,X = map(int,input().split())
A = list(map(int,input().split()))

s = set(A)

for a in A:
    if a + X in s:
        print("Yes")
        exit()
print("No")