N = int(input())
S = list(input())

for i in range(N-2):
    if S[i:i+3] == ["a","x","a"]:
        S[i] = S[i+1] = S[i+2] = "."
    elif S[i:i+3] == ["i","x","i"]:
        S[i] = S[i+1] = S[i+2] = "."
    elif S[i:i+3] == ["u","x","u"]:
        S[i] = S[i+1] = S[i+2] = "."
    elif S[i:i+3] == ["e","x","e"]:
        S[i] = S[i+1] = S[i+2] = "."
    elif S[i:i+3] == ["o","x","o"]:
        S[i] = S[i+1] = S[i+2] = "."

print("".join(S))