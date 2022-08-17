from collections import defaultdict

N =int(input())
A = list(map(int,input().split()))
dict = defaultdict(int)
for a in A:
    dict[a] += 1
s = set(A)
A = sorted(list(s))

ans = 0
for aj in A:
    for ak in A:
        if aj*ak > 2*(10**5):
            break
        ans += dict[aj]*dict[ak]*dict[aj*ak]

print(ans)