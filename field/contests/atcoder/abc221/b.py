S = list(input())
T = list(input())

if S == T:
    print("Yes")
else:
    for i in range(len(S)-1):
        S2 = S[:]
        S2[i],S2[i+1] = S2[i+1],S2[i]

        if S2 == T:
            print("Yes")
            break
    else:
        print("No")
