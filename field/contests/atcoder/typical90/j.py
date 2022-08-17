N = int(input())
score = [list(map(int,input().split())) for _ in range(N)]

cumsum_1 = [0]*(N+1)
cumsum_2 = [0]*(N+1)
for i in range(N):
    if score[i][0] == 1:
        cumsum_1[i+1] = cumsum_1[i] + score[i][1]
        cumsum_2[i+1] = cumsum_2[i]
    elif score[i][0] == 2:
        cumsum_1[i+1] = cumsum_1[i]
        cumsum_2[i+1] = cumsum_2[i] + score[i][1]

print(cumsum_1,cumsum_2)
Q = int(input())
query = [list(map(int,input().split())) for _ in range(Q)]
for q in query:
    l,r = q
    A = cumsum_1[r] - cumsum_1[l-1]
    B = cumsum_2[r] - cumsum_2[l-1]
    print(A,B)