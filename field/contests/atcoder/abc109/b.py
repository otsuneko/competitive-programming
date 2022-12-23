N =int(input())
W =[input() for _ in range(N)]

ans=True
cur = W[0]
seen = set([cur])
for w in W[1:]:
    if w in seen or w[0] != cur[-1]:
        ans = False
        break
    seen.add(w)
    cur = w

print(["No","Yes"][ans])