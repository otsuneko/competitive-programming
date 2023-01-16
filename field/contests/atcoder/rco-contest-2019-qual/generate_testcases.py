import subprocess
BASH = '/bin/bash'

for i in range(4,51):
    cmd = 'python3 generator.py {0} > ./testcases/b/in/input_{0}.txt'.format(str(i))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE, executable=BASH)