# https://www.geeksforgeeks.org/algorithms-gq/bit-algorithms-gq/bitwise-algorithms-intermediate/

def getBit(n,i):
    return 1 if (n & (1 << i)) else 0

def setBit(n,i):
    return n | (1 << i)

def toggleBit(n,i):
    return n ^ (1 << i)

def clearBit(n,i):
    return n & ~(1 << i)

def countSetBits(n):
    cnt = 0
    while n:
        cnt += 1
        n &= (n-1)
    return cnt

def FlippedCount(a,b):
    '''
    aとbを一致させるために反転させる必要があるビットの数を計算
    '''
    return countSetBits(a^b)

def maxConsecutiveOnes(n):
    '''
    nを2進数表現した時に最大で1が何連続で現れるか
    '''
    cnt = 0
    while (n!=0):
        n &= (n << 1)
        cnt=cnt+1      
    return cnt

def stripLowestSetBit(n):
    '''
    nを2進数表現した時に最右の1を0にする
    '''
    return n&n-1

def lowestSetBit(n):
    '''
    nを2進数表現した時に最右の1が立っているビットiに対する2^iを返す
    '''
    return n & -n

def isPowerOfTwo(n):
    '''
    n(>0)が2の冪乗かO(1)で判定(Brian Kernighan's algorithm) 例:4&3=0(100&011=0)
    '''
    return True if n and not n&(n-1) else False

def getPrevPowerOfTwo(n):
    '''
    n以下の最大の2冪を返す
    '''
    if isPowerOfTwo(n):
        return n
    return 0 if n == 0 else int("1" + (len(bin(n)[2:])-1)*"0", 2)

def getNextPowerOfTwo(n):
    '''
    n以上の最小の2冪を返す
    '''
    if isPowerOfTwo(n):
        return n
    return 1 if n == 0 else int("1" + (len(bin(n)[2:]))*"0", 2)

def isAllBitsSet(n):
    '''
    nを2進数表現した時に全てのビットが立っているか(2^k-1か)
    '''
    return True if n and not (n+1)&n else False

def isBitsInAltOrder(n):
    '''
    nを2進数表現した時に1と0が交互になっているか
    '''
    return isAllBitsSet(n^(n >> 1))

def isBitsSparse(n):
    '''
    nを2進数表現した時に1が連続する箇所がない(Sparce)か
    '''
    return False if (n & (n>>1)) else True

def swapBits(n,p1,p2,l):
    '''
    数字nの右からp1番目からlビットと、p2番目からlビットを入れ替える
    '''
    xor = (((n >> p1) ^ (n >> p2)) & ((1 << l) - 1))
    return n ^ ( (xor << p1) | (xor << p2))

# A+B = A^B + 2(A&B)
# A^Bは繰り上がりのない足し算と等価。
# 2(A&B)は、繰り上がり箇所を1ビット左シフトすることで繰り上がりを表現。

def TwoSetBitNums(n):
    '''
    2進数表現した時に1のビットが2個立っている数字のうち小さい方からn個を返す
    '''
    res = []
    x = 1
    while 1:
        y = 0
        while y < x:
            res.append((1 << x) + (1 << y))
            y += 1
            if len(res) == n:
                return res
        x += 1
    return res

def countGreaterXOR(n):
    '''
    0<x<nのxのうち、x^n>nとなるようなxの個数を返す
    '''
    k = 0
    cnt = 0
    while n > 0:
        if (n&1) == 0:
            cnt += pow(2,k)
        k += 1
        n >>= 1
    return cnt

def rangeAND(a,b):
    '''
    a,a+1,...,b-1,bまでの全てのAND
    '''
    if a > b:a,b = b,a
    shiftcnt=0
    while(a!=b and a>0):
        shiftcnt=shiftcnt+1
        a=a>>1
        b=b>>1
    return a<<shiftcnt

def allXOR(n):
    '''
    1からnまでの全てのXOR
    '''
    if n%4 == 0:
        return n
    elif n%4 == 1:
        return 1
    elif n%4 == 2:
        return n+1
    elif n%4 == 3:
        return 0

def sumXOR(arr,bit_len,mod=0):
    '''
    配列の任意の2要素のxorの和(例：[a,b,c]の場合…a^b+a^c+b^c)
    arr:処理対象の配列
    bit_len:bitの最大桁数
    mod:合計値のmodを取る場合はそのmod値(任意)
    '''
    res = 0
    # 2進表現の桁毎に処理
    for i in range(bit_len):
        zero_cnt = one_cnt = 0 # ある桁の1の個数と0の個数
        for j in range(len(arr)):
            if arr[j]%2 == 0:
                zero_cnt += 1
            else:
                one_cnt += 1
            arr[j] //= 2

        digsum = zero_cnt * one_cnt * (1 << i) # xorを1にできるパターン数(片方0でもう片方が1)×その桁の2冪
        
        if mod:
            res = (res+digsum)%mod
        else:
            res += digsum
    return res

# N,C = map(int,input().split())
# OP = [list(map(int,input().split())) for _ in range(N)]

# op = 0
# for t,a in OP:
#     if t == 1:
#         op &= a
#     elif t == 2:
#         op |= a
#     elif t == 3:
#         op ^= a
    