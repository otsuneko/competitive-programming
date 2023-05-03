from re import sub
import subprocess

infile = open("result.txt","r")
lines = infile.readlines()

outfile = open("score.txt","w")

for line in lines:
    if "Score" in line:
        score = line.replace("Score = ","")
        outfile.write(score)

infile.close()
outfile.close()