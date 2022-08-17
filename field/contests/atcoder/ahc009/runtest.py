from re import sub
import subprocess

for i in range(100):
    cmd = "python a.py < tools_x86_64-pc-windows-gnu\\in\\{}.txt > out{}.txt".format(str(i).zfill(4),str(i))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)