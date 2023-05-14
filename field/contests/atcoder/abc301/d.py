S = list(input())
N = int(input())

n = 0
for i in range(len(S)):
    n += (S[i] == "1") << (len(S)-1-i)

if n > N:
    print(-1)
    exit()

for i in range(len(S)):
    if S[i] == "?":
        add = (1 << (len(S)-1-i))
        if n + add > N:
            continue
        else:
            n += add
print(n)