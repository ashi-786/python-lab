import requests
from bs4 import BeautifulSoup as bs
import re
import concurrent.futures
import json

base_url = "https://www.point2homes.com"
# url = "https://www.point2homes.com/MX/Real-Estate-Listings/Quintana-Roo.html"
url = "https://www.point2homes.com/MX/Real-Estate-Listings.html"
# Proxy configuration with login and password
# proxy_host = 'gw.dataimpulse.com'
# proxy_port = 823
# proxy_login = 'ad233771e91039eb4781'
# proxy_password = '42130fb979e942e3'
# proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'
# r = requests.get(url, proxies={'http': proxy, 'https': proxy})

r = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': 'f1bd630d-7af0-4123-b4dd-6c8010bed171',
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

keys = ['title', 'price', 'price-drop', 'Latitude', 'Longitude', 'image-list', 'open-house-label', 'original-listing', 'Beds', 'Baths', 'Area', 'Lot-size ', 'Property-Type', 'Property-Summary', 'Property-Details', 'Description', 'Features', 'Price-History', 'Agent-Link']

def get_links(city, page):
    r = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': 'f1bd630d-7af0-4123-b4dd-6c8010bed171',
            'url': city+f"?page={page}",
            'bypass': 'cloudflare_level_1',
        },
    )
    # print(r.status_code)
    soup = bs(r.content, "html.parser")
    lis = soup.find("div", {'class': 'listings'}).find_all("div", {'class': 'item-cnt'})
    for li in lis:
        estate_links.append(base_url+li.find("a", string="View Details").get('href'))
    print(page)
    # if not soup.find("nav", {'aria-label': 'pagination'}).find("li", class_='next'):
    #     return 0

def get_data(link):
    try:
        # print(f"\nScraping {link}\n")
        vals = []
        res = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': 'f1bd630d-7af0-4123-b4dd-6c8010bed171',
                'url': link,
                'bypass': 'cloudflare_level_1',
            },
        )
        # print(res.status_code)
        soup2 = bs(res.content, "html.parser")
        main_content = soup2.find("main")
        title = main_content.find("div", class_="property-address").h1.text.strip()
        vals.append(title)
        try:
            price_str = main_content.find("div", class_="price").text.split("USD")[0].replace(",", "")
            price = int(re.sub(r"[^\d]", "", price_str))
        except: price = ""
        vals.append(price)
        try:
            price_drop = main_content.find("span", class_="price-drop").text
        except: price_drop = "" # no price-drop
        vals.append(price_drop)
        try:
            Latitude = float(main_content.find('input', id=lambda value: value and value.startswith("Latitude_l")).get('value'))
        except: Latitude = ""
        vals.append(Latitude)
        try:
            Longitude = float(main_content.find('input', id=lambda value: value and value.startswith("Longitude_l")).get('value'))
        except: Longitude = ""
        vals.append(Longitude)
        img_lis = main_content.find("div", id="details-photos-slider").find_all("li")
        imgs = [img.find("img").get('src') for img in img_lis]
        vals.append(imgs)
        try:
            open_house = main_content.find("div", class_="open-house-cnt").find("div", class_="open-house-right").text.strip()
        except: open_house = ""
        vals.append(open_house)
        try:
            original_listing = main_content.find("a", string="Original Listing").get('href')
        except: original_listing = ""
        vals.append(original_listing)
        # Property-Summary
        chars_lis = main_content.find("div", class_="characteristics-cnt")
        for clas in ["ic-beds", "ic-baths", "ic-sqft", "ic-lotsize", "ic-proptype"]:
            try:
                vals.append(chars_lis.find("li", class_=clas).text.strip())
            except: vals.append("")
        # Property-Details
        try:
            details = main_content.find("div", class_="property-details").find("div", class_="details-charcs")
            chr_dict = {}
            for dl in details.find_all("dl"):
                try:
                    chr_dict.update({dl.dt.text.strip() : dl.dd.text.strip()})
                except: pass
            vals.append(chr_dict)
        except: vals.append("")
        try:
            description = main_content.find("div", class_="description-full-cnt").find("div", class_="description-text").text.strip()
        except: description = ""
        vals.append(description)
        # Features
        try:
            features = main_content.find("div", class_="features-list").find_all("div", class_="features-col")
            chr_dict = {}
            for ftr in features:
                key = ftr.find("div", class_="features-list-title").text.strip()
                vals2 = [f.text.strip() for f in ftr.find_all("li")]
                chr_dict.update({key : list(vals2)})
            vals.append(chr_dict)
        except: vals.append("")
        # price-history
        try:
            hist_table = main_content.find("table", class_="price-history-tbl")
            history = []
            thList = [th.text.strip() for th in hist_table.find_all("th")]
            for tr in hist_table.tbody.find_all("tr"):
                tdList = [td.text.strip() for td in tr.find_all("td")]
                history.append({thList[i]:tdList[i] for i in range(len(thList))})
            vals.append(history)
        except: vals.append("")# no history

        # Agent-Link
        agents = soup2.find("aside", class_="content-side").find("div", class_="contacts_agents")
        contacts = agents.find("ul", class_="agent-links")
        profile_link = base_url+contacts.find("a", class_="ic-profile").get('href')
        vals.append(profile_link)
        for agent in agents:
            if agent['profile-link'] != profile_link:
                chr_dict = {}
                try: # agent-photo
                    chr_dict.update({'agent-photo': agents.find("img", class_="profile").get('src')})
                except: pass
                try: #agent-name
                    chr_dict.update({'agent-name': agents.find("div", class_="agent-name").text.strip()})
                except: pass
                try: #detail
                    chr_dict.update({'agent-detail': agents.find("div", class_="agent-name").find_next("p").text.strip()})
                except: pass
                try: #company-logo
                    chr_dict.update({'company-logo': agents.find("img", class_="company-logo").get('src')})
                except: pass
                
                try: #phone-list
                    phones = [link.get('data-phone') for link in contacts.find_all("span", class_="ic-phone")]
                    chr_dict.update({'phone-list': phones})
                except: pass
                try: #address
                    chr_dict.update({'address': contacts.find("span", class_="ic-map").text.strip()})
                except: pass
                try: #website
                    chr_dict.update({'website': contacts.find("a", class_="ic-website").get('href')})
                except: pass
                chr_dict.update({'profile-link': profile_link}) #profile-link
                agents.append(chr_dict)
        
        data_list.append({keys[i]:vals[i] for i in range(len(keys))})    
    except:
        data_list.append({"Error in": link})

for city, name in cities_link[0: 2], cities_name[0: 2]:
    estate_links = []
    agents = []
    data_list = []
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_links, city, [i for i in range(1, 3)])
            # Each city can currently have a maximum of 30 listings pages and every page has 24 Properties
    except: pass
    print(estate_links)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_data, estate_links[0: 3])
        # Iterate through all Property Listings in a city
    print(len(agents))
    print(len(data_list))
    with open(f"{name}.json", "w", encoding="utf-8") as f:
        json.dump({'Agents': agents, 'Properties': data_list}, f, ensure_ascii=False, indent=4)