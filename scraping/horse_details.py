import requests
from bs4 import BeautifulSoup
# import re
# import json

url = "https://www.ehorses.com/Homepage/HorsesResults"
base_url = "https://www.ehorses.com"
payload = f"Owner.Id=1455892&horseFilter.ProfilID=1455892&HorsesPerPage=10&seite={1}"
header = {
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'referer': 'https://www.ehorses.com/caballoria?page=horses&type=0',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

r = requests.request("POST", url, headers=header, data=payload)
# print(r.status_code)
soup = BeautifulSoup(r.content, "html.parser")
# print(soup.prettify())
main_divs = soup.find_all("div", class_="ownHorses")
main_links = [base_url+div.find("a").get("href") for div in main_divs]
print(main_links)
keys = ["headline", "horse_id", "img_list", "price"]
# main_list = []
for link, div in main_links, main_divs:
    res = requests.get(link)
    print(res.status_code)
    soup2 = BeautifulSoup(res.content, "html.parser")
    vals = []
    data = soup2.find("div", {'id': 'details'})
    vals.append(data.find("h1", class_="headline").text) #headline
    print(vals)
    vals.append(div.get("id")) #horse_id
    print(vals)
    img_list = [pic.get('href') for pic in data.find("div", {'id': 'media'}).find_all("a", class_="picItem")]
    vals.append(img_list) #imgs
    print(vals)
    vals.append(div.find("div", class_="priceTag").text.strip()) #price
    print(vals)
    rows = data.find("div", class_="moreDetails").find_all("div", class_="row")
    for row in rows: #more_details
        keys.append(row.find("label").text.replace(" ", "_"))
        if row.find("label").text == "more disciplines":
            vals.append([a.text for a in row.find("span").find_all("a")])
        elif row.find("label").text == "Further Characteristics":
            vals.append(row.find("span").stripped_strings)
        else:
            vals.append(row.find("span").text)
    print(keys)
    print(vals)
    desc = data.find("div", {'id': 'description'})
    keys.append(desc.find("h3").text.strip())
    vals.append(desc.find("div", class_="desc_en").find("pre").text.strip()) #description
    print(vals)
    keys.append("further_info")
    vals.append(data.find("div", class_='description').text.strip()) #further_info
    print(vals)
    break

# main_list.append({keys[i]:vals[i] for i in range(len(keys))})

# # # print(main_list)
# with open('horse_details.json', 'w', encoding="utf-8") as f:     
#         json.dump({"horse": main_list}, f, ensure_ascii=False, indent=4)