S = input()

dic = {}

def int_to_upper(k):
    return chr(k+65)

for i in range(26):
    dic[int_to_upper(i)] = i+1

ans = 0
for i,s in enumerate(S[::-1]):
    ans += dic[s]*26**i

print(ans)