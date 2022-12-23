N,K = map(int,input().split())
A = list(map(int,input().split()))

snack = [K//N]*N

order = []
for i in range(N):
    order.append([i,A[i]])

from operator import itemgetter
order.sort(key=itemgetter(1))

for i in range(K-(K//N)*N):
    snack[order[i][0]] += 1

for s in snack:
    print(s)