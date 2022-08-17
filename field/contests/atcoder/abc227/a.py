N,K,A = map(int,input().split())

person = A-1
for i in range(K):
    person += 1
    if person == N+1:
        person = 1

print(person)