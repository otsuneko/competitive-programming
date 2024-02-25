from re import sub
import subprocess

out = open("N_M_EPS.txt","w")

for i in range(100):
    f = open("tools/in/{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    nme = f.readline()
    nme = nme.replace(" ",",")
    out.write(nme[:9])
    out.write("\n")

    f.close()

out.close()