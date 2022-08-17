N,K,Q = map(int,input().split())

correct = [0]*N
for _ in range(Q):
    correct[int(input())-1] += 1

for c in correct:
    if K - (Q-c) > 0:
        print("Yes")
    else:
        print("No")