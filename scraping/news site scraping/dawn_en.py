import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from datetime import datetime
import json
import re
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
BASE_URL = "https://www.dawn.com/latest-news"
semaphore = asyncio.Semaphore(10)

time_formats = [
    "%B %d, %Y",
    "%d %B %Y",
    "%d %B, %Y",
    "%Y-%m-%d",
    "%b %d, %Y",
    "%d %b %Y",
    "%d %b, %Y",
]

def get_news_list():
    # print("[INFO] Fetching latest news list...")
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    all_news = soup.select("div.tabs__content div#all article")
    news_list = []

    for i, news in enumerate(all_news, 1):
        title = news.select_one("h2")
        short_desc = news.select_one("div.story__excerpt")
        link = news.select_one("a[href]")
        image = news.select_one("img")
        # summary = news.select_one("div.story__excerpt")
        # print(summary)

        article = {
            "title": title.get_text(strip=True) if title else "",
            "short_desc": short_desc.get_text(strip=True) if short_desc else "",
            "link": link['href'] if link else "",
            "thumbnail_image": image['data-src'] if image else "",
        }
        # print(f"[LIST] #{i} Parsed: {article['title']}")
        news_list.append(article)

    # print(f"[INFO] Found {len(news_list)} articles.")
    return news_list

async def fetch_detail(session: aiohttp.ClientSession, article: dict):
    async with semaphore:
        url = article['link']
        try:
            print(f"[FETCH] Starting: {url}")
            async with session.get(url, headers=headers, timeout=30, ssl=False) as res:
                if res.status == 403:
                    print(f"[WARN] 403 received for {url}, retrying after 2s...")
                    await asyncio.sleep(2)
                    async with session.get(url, headers=headers, timeout=30, ssl=False) as res_retry:
                        res = res_retry  # use the retried response

                print(f"Status code: {res.status}")
                html = await res.text()
                soup = BeautifulSoup(html, 'lxml')

                author = soup.select_one("span.story__byline")
                article["author"] = author.get_text(strip=True) if author else ""

                time_text = soup.select_one("span.timestamp--date") or soup.select_one("span.story__time")
                raw_time = time_text.get_text(strip=True) if time_text else ""
                parsed_time = ""
                for fmt in time_formats:
                    try:
                        dt = datetime.strptime(raw_time, fmt)
                        parsed_time = dt.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
                article["time"] = parsed_time
                article["main_img"] = ""

                body = soup.select_one("div.story__content")
                article["content"] = clean_html_content(body).decode_contents() if body else ""

                print(f"[FETCHED] Done: {article['title']}")

        except Exception as e:
            article["author"] = ""
            article["time"] = ""
            article["main_img"] = ""
            article["content"] = ""
            print(f"[ERROR] Failed to fetch {url} -> {e}")

async def run_all(news_list):
    print(f"[INFO] Fetching details for {len(news_list)} articles...")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_detail(session, article) for article in news_list]
        await asyncio.gather(*tasks)
    print("[INFO] All article details fetched.")

if __name__ == "__main__":
    print("[START] Scraper Started")

    news_list = get_news_list()
    asyncio.run(run_all(news_list))

    print("[SAVE] Writing results...")
    with open('dawn_en.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print("[DONE] All done. Output saved")