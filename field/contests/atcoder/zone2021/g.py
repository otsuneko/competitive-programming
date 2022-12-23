def rot13(S):
    S = list(S)
    for i in range(len(S)):
        ascii = ord(S[i])
        if ascii < 110:
            ascii += 13
        else:
            ascii -= 13
        S[i] = chr(ascii)
    return S

while True:
    try:
        S = input()
        print("".join(rot13(S)))

    except EOFError:
        break