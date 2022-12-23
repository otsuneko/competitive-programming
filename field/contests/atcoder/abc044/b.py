alphabet = dict.fromkeys("abcdefghijklmnopqrstuvwxyz",0)

w = input()
for c in w:
    alphabet[c] += 1

for key in alphabet:
    if alphabet[key]%2:
        print("No")
        break
else:
    print("Yes")