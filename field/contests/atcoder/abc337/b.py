import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def RunLengthEncoding(S):
    cur = S[0]
    cnt = 1
    res = []
    for i in range(1,len(S)):
        if cur == S[i]:
            cnt += 1
        else:
            res.append((cur,cnt))
            cur = S[i]
            cnt = 1
    res.append((cur,cnt))
    return res

S = input()
rle = RunLengthEncoding(S)

flg = False

if S == "":
    flg = True
elif len(rle) == 1 and rle[0][0] in ["A","B","C"]:
    flg = True
elif len(rle) == 2 and ((rle[0][0] == "A" and rle[1][0] == "B") or (rle[0][0] == "A" and rle[1][0] == "C") or (rle[0][0] == "B" and rle[1][0] == "C")):
    flg = True
elif len(rle) == 3 and rle[0][0] == "A" and rle[1][0] == "B" and rle[2][0] == "C":
    flg = True

print(["No","Yes"][flg])