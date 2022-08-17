import itertools
N = list(input())

ptr = list(itertools.permutations(N))

ans = 0
for p in ptr:
    for i in range(1,len(N)):
        n1 = p[:i]
        n2 = p[i:]

        if n1[0] != "0" and n2[0] != "0":
            ans = max(ans, int("".join(n1)) * int("".join(n2)))
print(ans)