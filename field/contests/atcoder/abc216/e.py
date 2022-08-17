N,K = map(int,input().split())
A = list(map(int,input().split())) + [0]
A.sort(reverse=True)

score = 0
height = A[0]
length = 1
for i in range(N):

    if K == 0:
        break

    for j in range(i+1,N+1):
        if height == A[j]:
            length += 1
        else:
            gap = height - A[j]
            break

    # while gap > 0:
    #     if length <= K:
    #         score += height * length
    #         K -= length
    #         height -= 1
    #         gap -= 1
    #     else:
    #         score += height * K
    #         K = 0
    #         break

    score += K//length*length + K%length
    K -= K//length*length + K%length
    

    length += 1

print(score)