S = list(input())

check = 0
for i in range(14):
    if i%2 == 0:
        check += int(S[i])
check *= 3

for i in range(14):
    if i%2 == 1:
        check += int(S[i])
check %=10

if check == int(S[14]):
    print("Yes")
else:
    print("No")