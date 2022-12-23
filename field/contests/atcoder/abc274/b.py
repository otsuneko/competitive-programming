H,W = map(int,input().split())
C = [list(input()) for _ in range(H)]

X = [0]*W

inv = list(zip(*C))

for i,l in enumerate(inv):
    X[i] = l.count("#")

print(*X)