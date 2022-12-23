K = int(input())

h = 21
if 0 <= K < 10:
    print(str(h) + ":0" + str(K))
elif 10 <= K < 60:
    print(str(h) + ":" + str(K))
elif 60 <= K < 70:
    print(str(h+1) + ":0" + str(K%60))
else:
    print(str(h+1) + ":" + str(K%60))
