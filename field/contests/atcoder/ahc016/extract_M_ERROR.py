from re import sub
import subprocess

out = open("M_ERROR.txt","w")

for i in range(100):
    f = open("tools\\in\\{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    nk = f.readline()
    nk = nk.replace(" ",",")
    out.write(nk)

    f.close()

out.close()