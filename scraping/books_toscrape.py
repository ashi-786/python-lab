import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
import json

base_url="https://books.toscrape.com/catalogue/"
url = "https://books.toscrape.com/"
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36']

with open("valid_proxies.txt", "r") as f:
    proxy = f.read().split("\n")
    proxies = [p for p in proxy]

main_list =[]
keys = ['Name', 'Img', 'Description', 'UPC', 'Product-Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews']
# for i in range(1, 51):
    # try:
    #     sleep(1)
p = choice(proxies)
r = requests.get(base_url + f"page-{1}.html", headers={'User-Agent': choice(user_agents)}, proxies={"http": p})
print(r.status_code)
soup = BeautifulSoup(r.content, "lxml")
articles = soup.find("ol", class_="row").find_all("article")
for article in articles:
    vals = []
    src = base_url + article.find_all("a")[0].get('href')
    try:
        sleep(1)
        p = choice(proxies)
        r = requests.get(src, headers={'User-Agent': choice(user_agents)}, proxies={"http": p})
        print(r.status_code)
        soup = BeautifulSoup(r.content, "lxml")
        page = soup.find("article", class_="product_page")
        vals.append(page.find("h1").text.strip())
        vals.append(url + page.find("div", class_="thumbnail").find("img").get('src').lstrip("../.."))
        vals.append(page.find("div", id="product_description").find_next("p").text.rstrip("...more"))
        tds = page.find("table").find_all("td")
        for td in tds:
            vals.append(td.text.strip())
        main_list.append({keys[j]:vals[j] for j in range(len(keys))})
    except:
        pass
    # except:
    #     pass

with open("books_toscrape.json", "w") as f:
    json.dump(main_list, f, indent=4)

# download all imgs
# i = 1
# for book in main_list:
#     downloaded = requests.get(book["Img"])
#     with open(f'img{i}.jpg','wb') as f:
#         f.write(downloaded.content)
#     i += 1
