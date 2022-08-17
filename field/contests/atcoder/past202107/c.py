S = input()
L,R = map(int,input().split())

flag = True

if str(int(S)) != S and S != "0":
    flag = False

if not (L <= int(S) <= R):
    flag = False

print(["No","Yes"][flag])