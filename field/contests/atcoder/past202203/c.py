# 0-indexed
def int_to_lower(k):
    return chr(k+97)

alpha =int(input())

l = len(str(alpha))
letter = (l-4)//3
top = (l-4)%3
print(str(alpha)[:top+1] + int_to_lower(letter))