from math import log2,ceil

S = list(input())
l = len(S)
Q =int(input())
alphabet = ["A","B","C"]

for _ in range(Q):
    t,k =map(int,input().split())
    k -= 1
    p = ceil(log2(k+1))
    if p < t:
        p = 2**p
        ori_chr_num = 0
        nth_chr = k
        ori_chr = S[ori_chr_num]
    else:
        p = 2**t
        ori_chr_num = int(k//p)
        nth_chr = k%p
        ori_chr = S[ori_chr_num]

    if ori_chr == "A":
        if t%3 == 0:
            if nth_chr == 0:
                print("A")
            elif nth_chr == p-1:
                print("C")
            else:
                print("B")
        elif t%3 == 1:
            if nth_chr == 0:
                print("B")
            elif nth_chr == p-1:
                print("A")
            else:
                print("C")
        elif t%3 == 2:
            if nth_chr == 0:
                print("C")
            elif nth_chr == p-1:
                print("B")
            else:
                print("A")
    elif ori_chr == "B":
        if t%3 == 0:
            if nth_chr == 0:
                print("B")
            elif nth_chr == p-1:
                print("A")
            else:
                print("C")
        elif t%3 == 1:
            if nth_chr == 0:
                print("C")
            elif nth_chr == p-1:
                print("B")
            else:
                print("A")
        elif t%3 == 2:
            if nth_chr == 0:
                print("A")
            elif nth_chr == p-1:
                print("C")
            else:
                print("B")
    elif ori_chr == "C":
        if t%3 == 0:
            if nth_chr == 0:
                print("C")
            elif nth_chr == p-1:
                print("B")
            else:
                print("A")
        elif t%3 == 1:
            if nth_chr == 0:
                print("A")
            elif nth_chr == p-1:
                print("C")
            else:
                print("B")
        elif t%3 == 2:
            if nth_chr == 0:
                print("B")
            elif nth_chr == p-1:
                print("A")
            else:
                print("C")
