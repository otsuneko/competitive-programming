S = input()
T = input()

cnt = sum([S[i] != T[i] for i in range(len(S))])
print(cnt)