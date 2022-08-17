S1 = input()
S2 = input()
S3 = input()

total = set(["ABC", "ARC", "AGC", "AHC"])
print(list(total - set([S1,S2,S3]))[0])