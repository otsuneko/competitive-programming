N = int(input())
S = input()

ans = 0
for i in range(1,N-1):
    f = set(list(S[:i]))
    l = set(list(S[i:]))
    ans = max(ans, len(f&l))
print(ans)