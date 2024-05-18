import requests
from bs4 import BeautifulSoup
import json

url = "https://www.hyipexplorer.com"
header = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36', }
req_data = {}

r = requests.get(url, headers = header)
soup = BeautifulSoup(r.content, "html.parser")

table1 = soup.find_all("table", attrs={'class': 'hyip', 'cellspacing': '0', 'cellpadding': '0'})

req_data['stickyw.gif'] = url + table1[1].find("img", attrs={'alt': 'sticky'}).get('src')
req_data['hyip-program'] = table1[1].find("a", class_=["hyip_program"]).text
req_data['star-rating'] = url + table1[1].find("img", attrs={'alt': '5 star rating'}).get('src')
req_data['reviews'] = table1[1].find("span", class_=["s9"]).text
req_data['status'] = table1[1].find("div", class_=["status"]).text
req_data['sslfree.gif'] = url + soup.find("img", attrs={'title': 'Free SSL valid: -211 days'}).get('src')

stats = list(soup.find_all("table", attrs={'cellspacing': '2', 'cellpadding': '2'}))[1]
req_data['stats'] = stats.text.strip()

desc = list(soup.find_all("div", class_=["even"]))[1]
req_data['shots'] = url + desc.img.get('src')
req_data['description'] = desc.text.strip()

link = list(soup.find_all("a", class_=["details"]))[1].get('href')
req_data['program details'] = url+link

monitored = list(soup.find_all("span", attrs={'class': 's9 gray'}))[1]
req_data['monitored'] = monitored.text.strip()

hbstatus = list(soup.find_all("div", class_=["a_"]))[1]
req_data['hbstatus'] = hbstatus.text.strip()

# download all imgs
all_imgs = [req_data['stickyw.gif'], req_data['star-rating'], req_data['sslfree.gif'], req_data['shots']]
i = 1
for img in all_imgs:
    downloaded = requests.get(img)
    with open(f'img{i}.jpg','wb') as f:
        f.write(downloaded.content)
    i += 1

with open('data.json', 'w') as f:     
    json.dump(req_data, f)
# print(req_data)
