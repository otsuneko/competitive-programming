S = input()

idx = S.index("SUNSET")
if idx+6 < len(S)-1:
    print(S[idx+6:]+S[:(idx+9)%len(S)])
else:
    print(S[idx+6:idx+9])
