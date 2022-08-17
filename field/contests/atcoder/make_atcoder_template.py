import os
import sys
import pathlib
args = sys.argv

if not args[1]:
    print("enter a contest name.")
    exit()

file_name = ["a", "b", "c", "d"]
cwd = os.getcwd()
contest_path = cwd + "/" + args[1]

if not os.path.exists(contest_path):
    # コンテストフォルダ作成
    os.mkdir(contest_path)

# ABC126以降は6問体制
if args[1][:3] == "abc" and int(args[1][3:]) >= 126:
    file_name += ["e", "f"]

# ABC212以降は8問体制
if args[1][:3] == "abc" and int(args[1][3:]) >= 212:
    file_name += ["g","h"]

# pythonファイル作成
for f in file_name:
    file_path = contest_path + "/" + f + ".py"
    if os.path.isfile(file_path):
        continue
    pathlib.Path(file_path).touch()