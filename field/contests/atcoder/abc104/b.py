S =input()

cnt_C = 0
for i,s in enumerate(S):
    if i == 0 and s != "A":
        print("WA")
        exit()
    if 2 <= i <= len(S)-2 and s == "C":
        cnt_C += 1
        if cnt_C > 1:
            print("WA")
            exit()
