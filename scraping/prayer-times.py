import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
import json

webcache = "https://webcache.googleusercontent.com/search?q=cache:"
url="www.islamic-relief.org.uk/resources/prayer-timetables/"
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36']

# scraper = cloudscraper.create_scraper()
# r = scraper.get(url, headers=header)

proxies = []
p = choice(proxies)
print(f"Using {p}")
try:
    r = requests.get(webcache+url, headers={'User-Agent': choice(user_agents)}, proxies={"http": f"http://{p}"})
    # print(r.status_code)
    soup = BeautifulSoup(r.content, "lxml")
    a = soup.find("div", class_="c-listings__cards").find_all("a")
    mkeys = [link.text.strip() for link in a]
    # print(mkeys)
    nkeys = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    links = [link.get('href').lstrip("https://") for link in a]
    main_dict = {}
    c = 0

    for url1 in links:
        pr = choice(proxies)
        print(f"Using {pr}")
        try:
            sleep(3)
            r = requests.get(webcache+url1, headers={'User-Agent': choice(user_agents)}, proxies={"http": f"http://{pr}"})
            print(r.status_code)
            soup = BeautifulSoup(r.content, "lxml")
            trs = soup.find("tbody").find_all("tr")
            # print(trs)
            values = []
            for tr in trs:
                values.append(tr.find_all("td")[1].text.strip())
            timing = {nkeys[i]: values[i] for i in range(len(nkeys))}
            print(timing)
            new = {mkeys[c]: timing}
            main_dict.update(new)
            # print(main_dict)
        except:
            new = {mkeys[c]: ""}
            main_dict.update(new)
            pass
        finally:
            c += 1
    with open('prayer-times.json', 'w') as f:     
        json.dump(main_dict, f, indent=4)
except:
    print("Failed")


