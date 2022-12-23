from collections import defaultdict
N,M = map(int,input().split())
S = list(map(int,input().split()))
X = set(list(map(int,input().split())))

S2 = [S[0]]
for i in range(1,N-1):
    S2.append(S[i]-S2[-1])

ans = 0
dict = defaultdict(int)
# A2~ANのどれをXと合わせるか
for i in range(N-1):
    # どのXと合わせるか
    for x in X:
        # iが奇数の時はA1 = X-S2[i]
        if i%2:
            A1 = x - S2[i]
        else:
            A1 = S2[i] - x
        dict[A1] += 1

for key in dict:
    if key in X:
        dict[key] += 1
    ans = max(ans,dict[key])

print(ans)