k = int(input())
s = input()

if len(s)<=k:
    print(s)
if len(s)>k:
    print(s[:k]+'...')