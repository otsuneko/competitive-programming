def binomialCoeff(n, k):

    res = 1
    for i in range(k):
        res = (res*(n-i))//(i+1)

    return res
 
    # # Declaring an empty array
    # C = [0 for i in range(k+1)]
    # C[0] = 1  # since nC0 is 1
 
    # for i in range(1, n+1):
 
    #     # Compute next row of pascal triangle using
    #     # the previous row
    #     j = min(i, k)
    #     while (j > 0):
    #         C[j] = C[j] + C[j-1]
    #         j -= 1
 
    # return C[k]

L = int(input())
print(binomialCoeff(L-1,11))
