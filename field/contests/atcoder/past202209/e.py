R,N,M,L = map(int,input().split())
S = list(map(int,input().split()))

rnd = 0
turn = 0
pin = 0
for s in S:
    pin += s
    turn += 1
    if pin > N:
        print("No")
        exit()
    elif pin == N or turn == M:
        rnd += 1
        pin = 0
        turn = 0

if rnd != R or turn != 0:
    print("No")
else:
    print("Yes")