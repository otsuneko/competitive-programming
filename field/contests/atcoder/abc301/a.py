N = int(input())
S = input()

if N%2:
    if S.count("T") > S.count("A"):
        print("T")
    else:
        print("A")
    exit()

taka = ao = 0
for i in range(N):
    if S[i] == "T":
        taka += 1
    else:
        ao += 1
    if taka == N//2:
        print("T")
        exit()
    elif ao == N//2:
        print("A")
        exit()