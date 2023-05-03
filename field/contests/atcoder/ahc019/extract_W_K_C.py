from re import sub
import subprocess

out = open("W_K_C.txt","w")

for i in range(100):
    f = open("tools/in/{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    nwkc = f.readline()
    nwkc = nwkc.replace(" ",",")
    out.write(nwkc[4:])

    f.close()

out.close()