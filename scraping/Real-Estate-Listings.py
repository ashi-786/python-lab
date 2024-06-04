import requests
from bs4 import BeautifulSoup as bs
import re
import concurrent.futures
import json

base_url = "https://www.point2homes.com"
url = "https://www.point2homes.com/MX/Real-Estate-Listings/Quintana-Roo.html"
links = []
keys = ['title', 'price', 'price-drop', 'Latitude', 'Longitude', 'image-list', 'open-house-label', 'original-listing', 'Property-Summary', 'Property-Details', 'Description', 'Features', 'Price-History', 'Agent-Details']
main_list = []
def get_links(page):
    r = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': 'API-KEY',
            'url': url+f"?page={page}",
            'bypass': 'cloudflare_level_1',
        },
    )
    # print(r.status_code)
    soup = bs(r.content, "html.parser")
    lis = soup.find("div", {'class': 'listings'}).find_all("div", {'class': 'item-cnt'})
    for li in lis:
        links.append(base_url+li.find("a", string="View Details").get('href'))
    

def get_data(link):
    try:
        # print(f"\nScraping {link}\n")
        vals = []
        res = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': 'API-KEY',
                'url': link,
                'bypass': 'cloudflare_level_1',
            },
        )
        # print(res.status_code)
        soup2 = bs(res.content, "html.parser")
        main_content = soup2.find("main")
        # title
        vals.append(main_content.find("div", class_="property-address").h1.text.strip())
        #price
        try:
            price = main_content.find("div", class_="price").text.split("USD")[0].replace(",", "")
            vals.append(int(re.sub(r"[^\d]", "", price)))
        except: vals.append("")
        # price-drop
        try:
            vals.append(main_content.find("span", class_="price-drop").text)
        except: vals.append("") # no price-drop
        # Latitude
        try:
            vals.append(float(main_content.find('input', id=lambda value: value and value.startswith("Latitude_l")).get('value')))
        except: vals.append("")
        # Longitude
        try:
            vals.append(float(main_content.find('input', id=lambda value: value and value.startswith("Longitude_l")).get('value')))
        except: vals.append("")
        # img-list
        imgs = main_content.find("div", id="details-photos-slider").find_all("li")
        vals.append([img.find("img").get('src') for img in imgs])
        # open house label
        try:
            vals.append(main_content.find("div", class_="open-house-cnt").find("div", class_="open-house-right").text.strip())
        except: vals.append("")
        # original-listing
        try:
            vals.append(main_content.find("a", string="Original Listing").get('href'))
        except: vals.append("")
        # Property-Summary
        vals.append([li.text.strip() for li in main_content.find("div", class_="characteristics-cnt").find_all("li")])
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
        # desc
        try:
            vals.append(main_content.find("div", class_="description-full-cnt").find("div", class_="description-text").text.strip())
        except: vals.append("")
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

        # Agent-Details
        agents = soup2.find("aside", class_="content-side").find("div", class_="contacts_agents")
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
        contacts = agents.find("ul", class_="agent-links")
        try: #phone-list
            phones = [link.get('data-phone') for link in contacts.find_all("span", class_="ic-phone")]
            chr_dict.update({'phone-list': phones})
        except: pass
        try: #website
            chr_dict.update({'website': contacts.find("a", class_="ic-website").get('href')})
        except: pass
        try: #profile-link
            chr_dict.update({'profile-link': base_url+contacts.find("a", class_="ic-profile").get('href')})
        except: pass
        vals.append(chr_dict)
        main_list.append({keys[i]:vals[i] for i in range(len(keys))})
    except:
        main_list.append({"Error in": link})

# Site has total 30 listings pages currently and every page has 24 Properties for sale
# which is going to make 720 requests using third-party proxy agregator
# Change the loop range as per the number of pages
try:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_links, [i for i in range(1, 3)])
except: pass
# print(len(links))

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_data, links)
# print(len(main_list))

with open("Real-Estate-Listings.json", "w", encoding="utf-8") as f:
    json.dump(main_list, f, ensure_ascii=False, indent=4)
