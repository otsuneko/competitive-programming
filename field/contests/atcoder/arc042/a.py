def sort_with_index(arr, reverse=False):
    if reverse:
        return sorted([ (x,i) for i, x in enumerate(arr)], reverse=True)
    else:
        return sorted([ (x,i) for i, x in enumerate(arr)])

N,M = map(int,input().split())
A = [int(input()) for _ in range(M)]

kaki = [-1]*N
zero = []
for i,a in enumerate(A):
    kaki[a-1] = i

for i,cnt in enumerate(kaki):
    if cnt == -1:
        zero.append(i)

kaki = sort_with_index(kaki,reverse=True)
# print(kaki,zero)

for cnt,idx in kaki:
    if cnt != -1:
        print(idx+1)
    else:
        break

for idx in zero:
    print(idx+1)