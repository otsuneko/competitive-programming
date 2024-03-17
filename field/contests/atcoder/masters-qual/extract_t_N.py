from re import sub
import subprocess

out = open("t_N.txt","w")

for i in range(50):
    f = open("tools/in/{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    tN = f.readline()
    tN = tN.replace(" ",",")
    out.write(tN[:9])

    f.close()

out.close()
