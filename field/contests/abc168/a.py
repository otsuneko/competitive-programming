n = input()
if int(n[-1]) in [2,4,5,7,9]:
    print('hon')
elif int(n[-1]) in [0,1,6,8]:
    print('pon')
elif int(n[-1])==3:
    print('bon')