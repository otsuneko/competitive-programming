N = int(input())
A = list(map(int,input().split()))

all = 0
for a in A:
    all ^= a

ans = []
for a in A:
    ans.append(str(a^all))

print(" ".join(ans))