import requests
from bs4 import BeautifulSoup as bs
import re
import concurrent.futures
import json

base_url = "https://www.point2homes.com"
url = "https://www.point2homes.com/MX/Real-Estate-Listings.html"
r = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': 'YOUR-API-KEY',
        'url': url,
        'bypass': 'cloudflare_level_1',
    },
)
# print(r.status_code)
soup = bs(r.content, "html.parser")
lis = soup.find_all("ul", {'class': 'list-region'})[1].find_all("li")
cities_name = [li.find("a").text.strip() for li in lis] # 33 cities
cities_link = [base_url+li.find("a").get('href') for li in lis]
with open("Cities-in-Mexico.json", "w", encoding="utf-8") as f:
    json.dump({cities_name[i]:cities_link[i] for i in range(len(cities_name))}, f, ensure_ascii=False, indent=4)

keys = ['property-detail-link', 'title', 'price', 'price-drop', 'latitude', 'longitude', 'image-list', 'open-house-label', 'original-listing', 'Beds', 'Baths', 'Area', 'Lot-size ', 'Property-Details', 'Description', 'Features', 'Price-History', 'Agent-Details']

def get_links(citypage):
    # print(citypage)
    r = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': 'YOUR-API-KEY',
            'url': citypage,
            'bypass': 'cloudflare_level_1',
        },
    )
    # print(r.status_code)
    soup = bs(r.content, "html.parser")
    lis = soup.find("div", class_='listings').find_all("div", {'class': 'item-cnt'})
    for li in lis:
        estate_links.append(base_url+li.find("a", string="View Details").get('href'))
    # if the pagination is less than 30
    # if not soup.find("nav", {'aria-label': 'pagination'}).find("li", class_='next'):
        

def get_data(link):
    try:
        vals = []
        vals.append(link)
        res = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': 'YOUR-API-KEY',
                'url': link,
                'bypass': 'cloudflare_level_1',
            },
        )
        # print(res.status_code)
        soup2 = bs(res.content, "html.parser")
        main_content = soup2.find("main")
        # title
        title = main_content.find("div", class_="property-address").h1.text.strip()
        # print(title)
        vals.append(title)
        try: # price
            price_str = main_content.find("div", class_="price").text.split(" ")[0].replace(",", "")
            vals.append(int(re.sub(r"[^\d]", "", price_str)))
        except: vals.append("")
        try: # price_drop
            vals.append(main_content.find("span", class_="price-drop").text)
        except: vals.append("") # no price-drop
        try: # latitude
            vals.append(float(main_content.find('input', id=lambda value: value and value.startswith("Latitude_l")).get('value')))
        except: vals.append("")
        try: # longitude
            vals.append(float(main_content.find('input', id=lambda value: value and value.startswith("Longitude_l")).get('value')))
        except: vals.append("")
        # imgs
        img_lis = main_content.find("div", id="details-photos-slider").find_all("li")
        imgs = [img.find("img").get('src') for img in img_lis]
        vals.append(imgs)
        try: # open-house-label
            vals.append(main_content.find("div", class_="open-house-cnt").find("div", class_="open-house-right").text.strip())
        except: vals.append("")
        try: # original_listing_link
            vals.append(main_content.find("a", string="Original Listing").get('href'))
        except: vals.append("")
        # Beds, Baths, Area, Lot-size, Property-Type
        chars_lis = main_content.find("div", class_="characteristics-cnt")
        for clas in ["ic-beds", "ic-baths", "ic-sqft", "ic-lotsize"]:
            try:
                chars_li = chars_lis.find("li", class_=clas).text.strip().replace(",", "")
                value = re.search(r'\d+(?:\.\d+)?', chars_li).group()
                if "." in value:
                    vals.append(float(value))
                else:
                    vals.append(int(value))
            except: vals.append("")
        # Property-Details
        try:
            details = main_content.find("div", class_="property-details").find("div", class_="details-charcs")
            chr_dict = {}
            for dl in details.find_all("dl"):
                try:
                    dt_key = dl.dt.text.strip().replace(" ", "-")
                    chr_dict.update({dt_key: dl.dd.text.strip()})
                except: pass
            vals.append(chr_dict)
        except: vals.append({})
        try: # description
            vals.append(main_content.find("div", class_="description-full-cnt").find("div", class_="description-text").text.strip())
        except: vals.append("")
        # Features
        try:
            features = main_content.find("div", class_="features-list").find_all("div", class_="features-col")
            chr_dict = {}
            for ftr in features:
                key = ftr.find("div", class_="features-list-title").text.strip().replace(" ", "-")
                vals2 = [f.text.strip() for f in ftr.find_all("li")]
                chr_dict.update({key : list(vals2)})
            vals.append(chr_dict)
        except: vals.append({})
        # price-history
        try:
            hist_table = main_content.find("table", class_="price-history-tbl")
            history = []
            thList = [th.text.strip() for th in hist_table.find_all("th")]
            for tr in hist_table.tbody.find_all("tr"):
                tdList = [td.text.strip() for td in tr.find_all("td")]
                history.append({thList[i]:tdList[i] for i in range(len(thList))})
            vals.append(history)
        except: vals.append([])# no history
        # Agent-Details
        contacts_agents = soup2.find("aside", class_="content-side").find("div", class_="contacts_agents")
        chr_dict = {}
        try: # agent-photo
            chr_dict.update({'agent-photo': contacts_agents.find("img", class_="profile").get('src')})
        except: pass
        try: #agent-name
            chr_dict.update({'agent-name': contacts_agents.find("div", class_="agent-name").text.strip()})
        except: pass
        try: #detail
            chr_dict.update({'agent-detail': contacts_agents.find("div", class_="agent-name").find_next("p").text.strip()})
        except: pass
        try: #company-logo
            chr_dict.update({'company-logo': contacts_agents.find("img", class_="company-logo").get('src')})
        except: pass
        contacts = contacts_agents.find("ul", class_="agent-links")
        try: #phone-list
            phonelist = contacts.find_all('li', class_=lambda value: value and value.startswith("phone-"))
            phones = []
            for phone in phonelist:
                ph_type = phone.find_all("span")[1].text.strip()[1:-1]
                ph_value = phone.find_all("span")[0].get('data-phone')
                ph_value = ''.join(char for char in ph_value if (char.isdigit() or char == '+'))
                phones.append({ph_type : ph_value})
            chr_dict.update({'phone-list': phones})
        except: pass
        try: #address
            chr_dict.update({'address': contacts.find("span", class_="ic-map").text.strip()})
        except: pass
        try: #website
            chr_dict.update({'website': contacts.find("a", class_="ic-website").get('href')})
        except: pass
        try:
            chr_dict.update({'profile-link': base_url+contacts.find("a", class_="ic-profile").get('href')})
        except: pass
        vals.append(chr_dict)
        # print(vals)
        data_list.append({keys[i]:vals[i] for i in range(len(keys))})
        # print(data_list)
    except:
        data_list.append({"Error in": link})

# citites = ['https://www.point2homes.com/MX/Real-Estate-Listings/Aguascalientes.html'] # to test for 1 city
for city in range(len(cities_link)):
    estate_links = []
    data_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_links, [cities_link[city]+f"?page={page}" for page in range(1, 31)])
        # Each city can have a maximum of 30 listings pages currently and every page has 24 Properties
    # print(len(estate_links))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_data, estate_links)
    # print(len(data_list))
    # with open(f"{'Aguascalientes'}.json", "w", encoding="utf-8") as f: # to test for 1 city
    with open(f"{cities_name[city]}.json", "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
