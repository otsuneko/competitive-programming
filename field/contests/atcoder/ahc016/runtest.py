from re import sub
import subprocess

li_lt005 = [1,46,91,35,22,6]
li_lt010 = [4,5,43,66,67,54]
li_lt015 = [49,99,20,19]
li_lt020 = [7,68,14,69,90]
li_lt025 = [60,81,31,32]
li_lt030 = [61,2,9,21,40,12,87]
li_lt035 = [98,8,25,38,26]
li_lt040 = [97,95,58,45,10,76,96]
for i in range(100):
# for i in li_lt040:
    cmd = "tools\\tester.exe pypy3 a.py < tools\\in\\{}.txt > tools\\out\\{}.txt".format(str(i).zfill(4),str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)