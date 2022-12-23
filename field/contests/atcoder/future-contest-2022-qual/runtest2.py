import subprocess

for i in range(10,20):
    cmd = 'cargo run --release --bin tester "C:\\Users\\otsuneko\\Documents\\GitHub\\competitive-programming\\tmp\\ahc003_a\\{}.txt" python a.py \> out.txt'.format(str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)