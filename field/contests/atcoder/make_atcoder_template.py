import os
import sys
import pathlib
import shutil
import subprocess
args = sys.argv

if not args[1]:
    print("enter a contest name.")
    exit()

folder_path = "/home/otsuneko/workspace/competitive-programming/field/contests/atcoder/"

# rustファイル作成
subprocess.run("cargo compete new {}".format(args[1]), shell=True, stdout = subprocess.PIPE)
subprocess.run("cargo member include {0}{1}".format(folder_path,args[1]), shell=True, stdout = subprocess.PIPE)

# pythonファイル作成
file_name = ["a", "b", "c", "d"]
contest_path = folder_path + args[1]
if not os.path.exists(contest_path):
    print("folder does not exist.")
    exit()

# ABC126以降は6問体制
if args[1][:3] == "abc" and int(args[1][3:]) >= 126:
    file_name += ["e", "f"]

# ABC212以降は8問体制
if args[1][:3] == "abc" and int(args[1][3:]) >= 212:
    file_name += ["g","h"]

# ABC319以降は7問体制
if args[1][:3] == "abc" and int(args[1][3:]) >= 319:
    file_name.pop()

# pythonファイル作成
for f in file_name:
    file_path = contest_path + "/" + f + ".py"
    if os.path.isfile(file_path):
        continue
    shutil.copyfile(folder_path + "atcoder_template.py", file_path)
    # pathlib.Path(file_path).touch()