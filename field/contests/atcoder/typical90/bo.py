#10進数→n進数
def base10int(value, base):
    if value >= base:
        return base10int(value//base, base) + str(value % base)
    return str(value % base)

#n進数→10進数(前処理として、各桁の値を格納したリストが必要)
def decode(digits, base):
    value = 0
    for digit in digits:
        value = value * base + int(digit)
    return value

N,K = map(str,input().split())
base_8 = list(N)
K = int(K)

for _ in range(K):
    # 8->10
    base_10 = int("".join(base_8), 8)
    # 10->9
    base_9 = base10int(base_10, 9)
    # 9->8
    base_8 = ["5" if i == "8" else i for i in base_9]

print("".join(base_8))