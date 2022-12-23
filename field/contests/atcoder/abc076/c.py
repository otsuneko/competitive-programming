S2 = input()
T = input()

if len(T) > len(S2):
    print("UNRESTORABLE")
    exit()

cand = []
for i in range(len(S2)-len(T)+1):
    for j in range(len(T)):
        if S2[i+j] == "?":
            continue
        if S2[i+j] != T[j]:
            break
    else:
        tmp = S2[:i][:] + T[:] + S2[i+len(T):]
        cand.append(list(tmp))

if not cand:
    print("UNRESTORABLE")
    exit()

for i in range(len(cand)):
    for j in range(len(cand[i])):
        if cand[i][j] == "?":
            cand[i][j] = "a"

cand.sort()
print("".join(cand[0]))