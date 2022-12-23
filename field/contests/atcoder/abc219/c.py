X = input()
N = int(input())
S = []
dic = dict()
dic_inv = dict()
for i in range(len(X)):
    dic[X[i]] = i+1
    dic_inv[i+1] = X[i]

for _ in range(N):
    s = input()
    new = []
    for c in s:
        new.append(dic[c])
    S.append(new)
S.sort()

for s in S:
    ans = ""
    for c in s:
        ans += dic_inv[c]
    print(ans)