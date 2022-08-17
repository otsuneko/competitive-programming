S = set(list(input()))

alphabet = dict.fromkeys("abcdefghijklmnopqrstuvwxyz",0)

for a in alphabet:
    if a not in S:
        print(a)
        break
else:
    print("None")
