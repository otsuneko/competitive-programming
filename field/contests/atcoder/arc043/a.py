N,A,B = map(int,input().split())
S = [int(input()) for _ in range(N)]

ma,mi = max(S),min(S)
avg = sum(S)/N

if ma == mi:
    print(-1)
    exit()
P = B/(ma-mi)
Q = A-P*avg
print(P,Q)