N = int(input())

check = set([])
for i in range(1,N+1):
    S = input()
    if S not in check:
        print(i)
        check.add(S)