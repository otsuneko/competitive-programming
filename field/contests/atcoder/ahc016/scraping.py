import requests
from bs4 import BeautifulSoup

url = 'https://atcoder.jp/contests/ahc016/submissions/36688543'

response = requests.get(url)
html_text = response.text
soup = BeautifulSoup(html_text, 'html.parser')

outfile = open("score_KoD.txt","w")

scores = soup.find("th", class_="no-break")
nxt = scores.next_element
cnt = 0
while 1:
    score = nxt.string
    if "/ 1000000000" in nxt:
        score = score.replace(" / 1000000000","\n")
        outfile.write(score)
        cnt += 1
        if cnt == 2000:
            break
    nxt = nxt.next_element

outfile.close()