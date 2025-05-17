import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from datetime import datetime
import json
import re
from urllib.parse import unquote
import asyncio
import aiohttp

def clean_html_content(element):
    for tag in element.find_all(["script", "style", "iframe", "noscript"]):
        tag.decompose()
    for div in element.find_all("div"):
        if not div.get_text(strip=True) and not div.find(["img", "a", "p", "strong", "em"]):
            div.decompose()
    for comment in element.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in element.find_all(True):
        allowed_attrs = {}
        if tag.name == "a" and "href" in tag.attrs:
            allowed_attrs["href"] = tag["href"]
        elif tag.name == "img" and "src" in tag.attrs:
            allowed_attrs["src"] = tag["src"]
        tag.attrs = allowed_attrs
    return element

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}
BASE_URL = "https://gnnhd.tv/latest"
semaphore = asyncio.Semaphore(10)

# Mapping Urdu to English
urdu_months = {
    "جنوری": "January", "فروری": "February", "مارچ": "March",
    "اپریل": "April", "مئی": "May", "جون": "June",
    "جولائی": "July", "اگست": "August", "ستمبر": "September",
    "اکتوبر": "October", "نومبر": "November", "دسمبر": "December"
}

urdu_ampm = {
    "صبح": "AM",
    "شام": "PM"
}

def get_news_list():
    # print("[INFO] Fetching latest news list...")
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    all_news = soup.select("a.group")
    news_list = []

    for i, news in enumerate(all_news, 1):
        if not news:
            continue
        link = f"https://gnnhd.tv/{news['href']}"
        image_srcset = news.select_one("img").get("srcset") if news.select_one("img") else ""
        # Find the 1200w URL
        match = re.search(r'(/_next/image\?[^ ]+&w=1200[^ ]*)', image_srcset)
        if match:
            partial_url = match.group(1)
            full_url = "https://gnnhd.tv" + unquote(partial_url)
        else:
            full_url = ""

        article = {
            "link": link,
            "thumbnail_image": full_url,
        }
        # print(f"[LIST] #{i} Parsed: {article['title']}")
        news_list.append(article)

    # print(f"[INFO] Found {len(news_list)} articles.")
    return news_list

async def fetch_detail(session: aiohttp.ClientSession, article: dict):
    async with semaphore:
        try:
            # print(f"[FETCH] Starting: {article['link']}")
            async with session.get(article['link'], headers=headers, timeout=30,ssl=False) as res:
                html = await res.text()
                soup = BeautifulSoup(html, 'lxml')

                title = soup.select_one("div#printable-area h1")
                article["title"] = title.get_text(strip=True) if title else ""
                author = soup.select_one("div#printable-area span.font-bold")
                # print(author)
                article["author"] = author.get_text(strip=True) if author else ""
                time_text = soup.select("div#printable-area strong.font-semibold")[1]
                # print(time_text)
                raw_time = time_text.get_text(strip=True) if time_text else ""
                
                # Replace Urdu month and AM/PM
                for urdu, eng in urdu_months.items():
                    raw_time = raw_time.replace(urdu, eng)

                for urdu, eng in urdu_ampm.items():
                    raw_time = raw_time.replace(urdu, eng)

                raw_time = raw_time.replace("،", ",")
                raw_time = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', raw_time)
                try:
                    dt = datetime.strptime(raw_time.strip(), "%B %d %Y, %I:%M %p")
                    article["time"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    article["time"] = ""

                main_img = soup.select_one("div#printable-area img.rounded-lg")
                article["main_image"] = f"https://gnnhd.tv/{main_img['src']}" if main_img else ""

                body = soup.select_one("div#printable-area div.prose")
                if body:
                    cleaned = clean_html_content(body)
                    article["content"] = cleaned.decode_contents()
                else:
                    article["content"] = ""

                # print(f"[FETCHED] Done: {article['title']}")

        except Exception as e:
            article["title"] = ""
            article["author"] = ""
            article["time"] = ""
            article["main_image"] = ""
            article["content"] = ""
            print(f"[ERROR] Failed to fetch {article['link']} -> {e}")

async def run_all(news_list):
    # print(f"[INFO] Fetching details for {len(news_list)} articles...")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_detail(session, article) for article in news_list]
        await asyncio.gather(*tasks)
    print("[INFO] All article details fetched.")

if __name__ == "__main__":
    print("[START] Scraper Started")

    news_list = get_news_list()
    asyncio.run(run_all(news_list))

    print("[SAVE] Writing results...")
    with open('gnn_en.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print("[DONE] All done. Output saved")