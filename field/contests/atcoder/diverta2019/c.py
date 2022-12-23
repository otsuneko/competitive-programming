N =int(input())
S =[input() for _ in range(N)]

BA = []
firstB = []
lastA = []
other = []

ans = 0
for s in S:
    if s[0] == "B" and s[-1] == "A":
        BA.append(s)
    elif s[0] == "B":
        firstB.append(s)
    elif s[-1] == "A":
        lastA.append(s)
    else:
        other.append(s)
    ans += s.count("AB")

ans += max(0,len(BA)-1)
if len(BA) > 0 and (len(firstB) > 0 or len(lastA) > 0):
    ans += min(len(firstB),len(lastA))+1
else:
    ans += min(len(firstB),len(lastA))
print(ans)