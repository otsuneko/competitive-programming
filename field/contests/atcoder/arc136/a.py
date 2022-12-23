N =int(input())
S = input()

idx = 0
S2 = []
while idx < len(S):
    if S[idx] == "A":
        S2.append("BB")
        idx += 1
    else:
        S2.append(S[idx])
        idx += 1

S = "".join(S2)

idx = 0
ans = []
while idx < len(S):
    if idx < len(S)-1 and S[idx] == "B" and S[idx+1] == "B":
        ans.append("A")
        idx += 2
    else:
        ans.append(S[idx])
        idx += 1

print("".join(ans))