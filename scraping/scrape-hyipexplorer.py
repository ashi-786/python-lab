import requests
from bs4 import BeautifulSoup
import json

url = "https://www.hyipexplorer.com"
header = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36', }
r = requests.get(url, headers = header)
soup = BeautifulSoup(r.content, "lxml")
table = soup.find("div", id="content").find_all("table")[9]

keys = ['img1', 'hyip-program', 'star-rating', 'reviews', 'status', 'ssl-img', 'stats', 'shots-img', 'desc', 'monitored', 'hbstatus']
values = []

# extracting data
values.append(url + table.find_all("img", attrs={'alt': 'sticky'})[1].get('src') if len(table.find_all("img", attrs={'alt': 'sticky'})) > 1 else "")
values.append(table.find("a", class_=["hyip_program"]).text if table.find("a", class_=["hyip_program"]) else "")
values.append(url + table.find_all("div", class_=["rating"])[1].img.get('src') if len(table.find_all("div", class_=["rating"])) > 1 else "")
values.append(table.find_all("div", class_=["rating"])[1].span.text if len(table.find_all("div", class_=["rating"])) > 1 else "")
values.append(table.find_all("div", class_=["status"])[1].text if len(table.find_all("div", class_=["status"])) > 1 else "")
values.append(url + table.find_all("img", attrs={'alt': 'Free SSL'})[1].get('src') if len(table.find_all("img", attrs={'alt': 'Free SSL'})) > 1 else "")
values.append(table.find_all("table", attrs={'cellspacing': '2', 'cellpadding': '2'})[1].text.strip() if len(table.find_all("table", attrs={'cellspacing': '2', 'cellpadding': '2'})) > 1 else "")
values.append(url + table.find_all("div", class_=["even"])[1].img.get('src') if len(table.find_all("div", class_=["even"])) > 1 else "")
values.append(table.find_all("div", class_=["even"])[1].text.strip() if len(table.find_all("div", class_=["even"])) > 1 else "")
values.append(table.find_all("span", attrs={'class': 's9 gray'})[1].text.strip() if len(table.find_all("span", attrs={'class': 's9 gray'})) > 1 else "")
values.append(table.find_all("div", class_=["a_"])[1].text.strip() if len(table.find_all("div", class_=["a_"])) > 1 else "")
# populating dictionary
req_data = {keys[i]: values[i] for i in range(len(keys))}
print(req_data)

# download all imgs
# i = 1
# for key, val in req_data.items():
#     if "/images" in req_data[key] or "/uploads" in req_data[key]:
#         downloaded = requests.get(req_data[key])
#         with open(f'img{i}.jpg','wb') as f:
#             f.write(downloaded.content)
#         i += 1

with open('data.json', 'w') as f:     
    json.dump(req_data, f, indent=4)