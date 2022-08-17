S = list(input())

flg = False
start_idx = 0
word_list = []
for i in range(len(S)):
    if S[i].isupper():
        if not flg:
            start_idx = i
            flg = not flg
        else:
            word_list.append("".join(S[start_idx:i+1]))
            flg = not flg

word_list.sort(key = str.lower)
print("".join(word_list))