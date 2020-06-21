k,n = map(int,input().split())
a_inputs = [int(a) for a in input().split()]

longest = a_inputs[0]+(k-a_inputs[-1])
for i in range(n-1):
    if a_inputs[i+1]-a_inputs[i]>longest:
        longest = a_inputs[i+1]-a_inputs[i]

print(k-longest)