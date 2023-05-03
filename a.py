N = int(input())
S = input()

if len(set(S)) == 1:
    print(1)
    exit()

if N%2:
    print(N)
    exit()

ans = 0
for i in range(1,N):
    if S[i] != S[i-1]:
        ans = i+1
        break

if N%ans != 0:
    print(N)
    exit()

T = S[:ans]
for i in range(0,N,ans):
    if S[i:i+ans] != T:
        print(N)
        exit()
print(ans)