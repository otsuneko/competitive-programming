from operator import itemgetter
N,K = map(int,input().split())
score = []
for _ in range(N):
    a,b = map(int,input().split())
    score.append(b)
    score.append(a-b)

score.sort(reverse=True)
print(sum(score[:K]))