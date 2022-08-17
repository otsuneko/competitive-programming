def sumXOR(arr,bit_len,mod=0):
    res = 0
    for i in range(bit_len):
        #  Count of zeros and ones
        zero_cnt = one_cnt = 0

        # Individual sum at each bit position
        dig_sum = 0
        for j in range(len(arr)):
            if arr[j]%2 == 0:
                zero_cnt += 1
            else:
                one_cnt += 1
            arr[j] //= 2

        # calculating individual bit sum
        idsum = zero_cnt * one_cnt * (1 << i)
  
        # final sum
        if mod:
            res = (res+idsum)%mod
        else:
            res += idsum

    return res

N = int(input())
A = list(map(int,input().split()))
mod = 10**9+7

print(sumXOR(A,60,mod))