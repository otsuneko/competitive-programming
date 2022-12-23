A,B,C = map(int,input().split())

i = 1
while i < 10**7:
    if A*i%B == C:
        print("YES")
        break
    i += 1
else:
    print("NO")