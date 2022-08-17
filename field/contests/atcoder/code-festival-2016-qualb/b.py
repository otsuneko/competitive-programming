N,A,B = map(int,input().split())
S = input()

passed = 0
abroad_rank = 0
for i in range(N):
    if S[i] == "a":
        if passed < A+B:
            passed += 1
            print("Yes")
        else:
            print("No")
    elif S[i] == "b":
        abroad_rank += 1
        if passed < A+B and abroad_rank <= B:
            passed += 1
            print("Yes")
        else:
            print("No")
    else:
        print("No")
    