N,K = map(int,input().split())
snuke = [False]*N
for _ in range(K):
    d = int(input())
    okashi = list(map(int,input().split()))
    for o in okashi:
        snuke[o-1] = True

print(snuke.count(False))