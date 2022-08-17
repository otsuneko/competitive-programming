N = int(input())
S = [input() for _ in range(N)]

dict = {"AC":0, "WA":0, "TLE":0, "RE":0}
for s in S:
    dict[s] += 1
for key in dict:
    print(key + " x " + str(dict[key]))