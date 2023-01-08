T = int(input())

for t in range(T):
    N = int(input())
    A = list(map(int,input().split()))

    print(len([a for a in A if a%2 == 1]))