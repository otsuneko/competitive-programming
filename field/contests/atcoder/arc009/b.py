# 0-indexed
def int_to_lower(k):
    return chr(k+97)

def int_to_upper(k):
    return chr(k+65)

def lower_to_int(c):
    return ord(c)-97

def upper_to_int(c):
    return ord(c)-65

B = list(map(str,input().split()))
N = int(input())
A =  [list(input()) for _ in range(N)]

dic = {}
dic_inv = {}
for i in range(10):
    dic[B[i]] = chr(i+65)
    dic_inv[chr(i+65)] = B[i]

A2 = []
for i in range(N):
    tmp = ""
    for c in A[i]:
        tmp += dic[c]
    A2.append(tmp)

A2.sort()
ans = []
for i in range(N):
    tmp = ""
    for c in A2[i]:
        tmp += dic_inv[c]
    ans.append(tmp)

for a in ans:
    print(a)