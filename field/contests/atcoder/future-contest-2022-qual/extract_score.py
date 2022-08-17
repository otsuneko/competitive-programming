path = 'score.in'

with open(path) as f:
    line = f.readlines()
f.close()

path_w = 'score.out'

with open(path_w, mode='w') as f:
    for txt in line:
        if "Score" in txt:
            l = txt.split()
            f.write(l[2] + "\n")
f.close()