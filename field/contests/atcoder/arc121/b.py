from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N = int(input())
dogs = {"R":[],"G":[],"B":[]}
for _ in range(2*N):
    a,c = map(str,input().split())
    dogs[c].append(int(a))

dogs["G"].sort()
dogs["B"].sort()

# Rが偶数になるように入れ替え(G,Bは偶,偶or奇,奇)
if len(dogs["R"])%2==0:
    pass
elif len(dogs["G"])%2==0:
    dogs["R"],dogs["G"] = dogs["G"],dogs["R"]
elif len(dogs["B"])%2==0:
    dogs["R"],dogs["B"] = dogs["B"],dogs["R"]

ans = 10**18
if len(dogs["G"])%2==0 and len(dogs["B"])%2==0:
    ans = 0
else:
    for d1 in dogs["G"]:
        idx = bisect_left(dogs["B"],d1)
        if 0 <= idx < len(dogs["B"]):
            ans = min(ans,abs(dogs["B"][idx]-d1))
        if 1 <= idx:
            ans = min(ans,abs(dogs["B"][idx-1]-d1))

    if len(dogs["R"]):
        tmp1=10**18
        for d1 in dogs["R"]:
            idx = bisect_left(dogs["B"],d1)
            if idx < len(dogs["B"]):
                tmp1 = min(tmp1,abs(dogs["B"][idx]-d1))
            if 1 <= idx:
                tmp1 = min(tmp1,abs(dogs["B"][idx-1]-d1))
        tmp2=10**18
        for d1 in dogs["R"]:
            idx = bisect_left(dogs["G"],d1)
            if idx < len(dogs["G"]):
                tmp2 = min(tmp2,abs(dogs["G"][idx]-d1))
            if 1 <= idx:
                tmp2 = min(tmp2,abs(dogs["G"][idx-1]-d1))
        ans = min(ans,tmp1+tmp2)            

print(ans)