# 0-indexed
def int_to_lower(k):
    return chr(k+97)

N = int(input())

ans = ""
while N > 0:
    N -= 1
    ans += int_to_lower(N%26)
    N //= 26

print(ans[::-1])

### original code ###
# N = int(input())
# N = N-1

# def kth_lower(k):
#     return chr(k+97)

# def kth_upper(k):
#     return chr(k+65)

# whole_idx = 0
# part_idx = 0
# l = 1
# while 1:
#     if whole_idx + 26**l > N:
#         break
#     whole_idx += 26**l
#     l += 1
# part_idx = N-whole_idx

# ans = ""
# for _ in range(l):
#     ans += kth_lower(part_idx%26)
#     part_idx //= 26

# print(ans[::-1])