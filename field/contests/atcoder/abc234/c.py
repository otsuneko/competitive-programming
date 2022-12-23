# 10進数⇒2,8,16進数
x = 10
bin_x = bin(x)[2:]
oct_x = oct(x)[2:]
hex_x = hex(x)[2:]

K =int(input())

ans = bin(K)[2:].replace("1","2")
print(ans)