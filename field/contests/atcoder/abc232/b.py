# 0-indexed
def int_to_lower(k):
    return chr(k+97)

def int_to_upper(k):
    return chr(k+65)

def lower_to_int(c):
    return ord(c)-97

def upper_to_int(c):
    return ord(c)-65

S = input()
T = input()

for k in range(26):
    S2 = []
    for s in S:
        S2.append(int_to_lower((lower_to_int(s)+k)%26))
    if T == "".join(S2):
        print("Yes")
        break
else:
    print("No")