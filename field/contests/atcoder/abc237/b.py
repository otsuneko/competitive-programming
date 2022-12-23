H,W =map(int,input().split())
A =[list(map(str,input().split())) for _ in range(H)]

B = list(zip(*A))

for i in range(W):
    print(" ".join(B[i]))