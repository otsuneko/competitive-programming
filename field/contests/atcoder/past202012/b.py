N = int(input())
S = input()
T = ""

for i in range(N):
    tmp = ""
    for j in range(len(T)):
        if T[j] != S[i]:
            tmp += T[j]
    tmp += S[i]
    T = tmp
print(T)