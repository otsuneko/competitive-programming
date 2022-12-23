from re import sub
import subprocess

def extract_scores(lines):
    scores = []
    for line in lines:
        scores.append(int(line))
    return scores

# nagissさんのスコア読み込み
infile = open("score_nagiss.txt","r")
lines = infile.readlines()
scores_nagiss = extract_scores(lines)
infile.close()

# sugarrrさんのスコア読み込み
infile = open("score_sugarrr.txt","r")
lines = infile.readlines()
scores_sugarrr = extract_scores(lines)
infile.close()

# ymatsuxさんのスコア読み込み
infile = open("score_ymatsux.txt","r")
lines = infile.readlines()
scores_ymatsux = extract_scores(lines)
infile.close()

# Shun_PIさんのスコア読み込み
infile = open("score_Shun_PI.txt","r")
lines = infile.readlines()
scores_Shun_PI = extract_scores(lines)
infile.close()

# shibh308さんのスコア読み込み
infile = open("score_shibh308.txt","r")
lines = infile.readlines()
scores_shibu308 = extract_scores(lines)
infile.close()

# 最高スコア(仮)を算出
scores_top = []
for s1,s2,s3,s4,s5 in zip(scores_nagiss, scores_sugarrr, scores_ymatsux, scores_Shun_PI, scores_shibu308):
    scores_top.append(max((s1,s2,s3,s4,s5)))

# stoqさんのスコア読み込み
infile = open("score_stoq.txt","r")
lines = infile.readlines()
scores_stoq = extract_scores(lines)
infile.close()

# takumi152さんのスコア読み込み
infile = open("score_takumi152.txt","r")
lines = infile.readlines()
scores_takumi152 = extract_scores(lines)
infile.close()

# y151さんのスコア読み込み
infile = open("score_y151.txt","r")
lines = infile.readlines()
scores_y151 = extract_scores(lines)
infile.close()

# youluoyさんのスコア読み込み
infile = open("score_youluoy.txt","r")
lines = infile.readlines()
scores_youluoy = extract_scores(lines)
infile.close()

# blackyukiさんのスコア読み込み
infile = open("score_blackyuki.txt","r")
lines = infile.readlines()
scores_blackyuki = extract_scores(lines)
infile.close()

# yurimoirさんのスコア読み込み
infile = open("score_yurimoir.txt","r")
lines = infile.readlines()
scores_yurimoir = extract_scores(lines)
infile.close()

# KoDさんのスコア読み込み
infile = open("score_KoD.txt","r")
lines = infile.readlines()
scores_KoD = extract_scores(lines)
infile.close()

# otsunekoのスコア読み込み
infile = open("score_otsuneko.txt","r")
lines = infile.readlines()
scores_otsuneko = extract_scores(lines)
infile.close()

# 相対スコア計算(nagissさんが全テストケースで最高得点と仮定)
rel_score_stoq = 0
rel_score_takumi152 = 0
rel_score_y151 = 0
rel_score_youluoy = 0
rel_score_blackyuki = 0
rel_score_yurimoir = 0
rel_score_KoD = 0
rel_score_otsuneko = 0
for i in range(2000):
    rel_score_stoq += round(10**9 * (scores_stoq[i]/scores_top[i]))
    rel_score_takumi152 += round(10**9 * (scores_takumi152[i]/scores_top[i]))
    rel_score_y151 += round(10**9 * (scores_y151[i]/scores_top[i]))
    rel_score_youluoy += round(10**9 * (scores_youluoy[i]/scores_top[i]))
    rel_score_blackyuki += round(10**9 * (scores_blackyuki[i]/scores_top[i]))
    rel_score_yurimoir += round(10**9 * (scores_yurimoir[i]/scores_top[i]))
    rel_score_KoD += round(10**9 * (scores_KoD[i]/scores_top[i]))
    rel_score_otsuneko += round(10**9 * (scores_otsuneko[i]/scores_top[i]))

# 結果書き出し

outfile = open("systes_score_assumption.txt","w")
outfile.write("stoq:{}".format(rel_score_stoq))
outfile.write("\n")
outfile.write("takumi152:{}".format(rel_score_takumi152))
outfile.write("\n")
outfile.write("y151:{}".format(rel_score_y151))
outfile.write("\n")
outfile.write("youluoy:{}".format(rel_score_youluoy))
outfile.write("\n")
outfile.write("blackyuki:{}".format(rel_score_blackyuki))
outfile.write("\n")
outfile.write("yurimoir:{}".format(rel_score_yurimoir))
outfile.write("\n")
outfile.write("KoD:{}".format(rel_score_KoD))
outfile.write("\n")
outfile.write("otsuneko:{}".format(rel_score_otsuneko))
outfile.close()
