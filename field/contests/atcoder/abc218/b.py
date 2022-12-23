P = list(map(int,input().split()))

# 0-indexed
def int_to_lower(k):
    return chr(k+97)

def int_to_upper(k):
    return chr(k+65)

def lower_to_int(c):
    return ord(c)-97

def upper_to_int(c):
    return ord(c)-65

ans = ""
for p in P:
    ans += int_to_lower(p-1)
print(ans)