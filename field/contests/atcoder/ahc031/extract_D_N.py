from re import sub
import subprocess

out = open("D_N.txt","w")

for i in range(100):
    f = open("tools/in/{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    dn = f.readline()
    dn = dn.replace(" ",",")
    out.write(dn[5:10])
    out.write("\n")

    f.close()

out.close()
