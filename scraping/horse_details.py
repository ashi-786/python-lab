import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://www.caballoria.com"

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
r = requests.get(url, headers=header)
soup = BeautifulSoup(r.content, "lxml")
# print(soup)
main_divs = soup.find_all("div", class_="comp-l610zaip")
keys = ["title", "description", "horse_id", "image_link", "category", "color", "gender", "race", "height", "suitablity", "education", "price", "age", "location", "x_ray", "full_papers"]
main_list = []
for div in main_divs:
    link = div.find_all("a")[0].get('href')
    vals = []
    ctg = div.find_all("p", {'class': 'font_8 wixui-rich-text__text'})
    res = requests.get(link, headers=header)
    # print(res.status_code)
    soup2 = BeautifulSoup(res.content, "lxml")
    # likes = soup2.find("div", id="pro-gallery-container-comp-l5z7shsl").get_text()
    data = soup2.find("section", id="comp-l5z6paxb").find_all("div", class_="HcOXKn")
    vals.append(data[0].get_text()) #title
    vals.append(data[-1].get_text()) #description
    vals.append(int(soup2.find("div", id="comp-ljbb0j4v").get_text())) #horse_id
    vals.append(soup2.find("div", id="pro-gallery-container-comp-l5z7shsl").find("img").get('src')) #img_link
    vals.append(ctg[0].get_text()) #category
    vals.append(data[10].get_text()) #color
    vals.append(data[6].get_text()) #gender
    vals.append(data[4].get_text()) #race
    vals.append(int(re.search(r"\d+", data[8].get_text()).group())) #height
    vals.append(list(data[15].get_text().split(", "))) #suitability
    vals.append(list(data[18].get_text().split(", "))) #education
    vals.append(data[-3].get_text()) #price
    vals.append(int(re.search(r"\d+", data[5].get_text()).group())) #age
    vals.append(data[-5].get_text()) #location
    vals.append(data[12].get_text()) #x_ray
    vals.append(data[14].get_text()) #full_papers
    main_list.append({keys[i]:vals[i] for i in range(len(keys))})

# # print(main_list)
with open('horse_details.json', 'w', encoding="utf-8") as f:     
        json.dump({"horse": main_list}, f, ensure_ascii=False, indent=4)