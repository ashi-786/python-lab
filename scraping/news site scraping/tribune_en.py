import asyncio
import aiohttp
from bs4 import BeautifulSoup
from bs4 import Comment
from datetime import datetime
import re
import json
import requests

def clean_html_content(element):
    for tag in element.find_all(["script", "style", "iframe", "noscript"]):
        tag.decompose()
    for div in element.find_all("div"):
        if not div.get_text(strip=True) and not div.find(["img", "a", "p", "strong", "em"]):
            div.decompose()
    # for comment in element.find_all(string=lambda text: isinstance(text, Comment)):
    #     comment.extract()
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
BASE_URL = "https://tribune.com.pk/latest"
semaphore = asyncio.Semaphore(10)

def get_news_list():
    print("[INFO] Fetching latest news list...")
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    all_news = soup.select("ul.listing-page li")
    news_list = []

    for i, news in enumerate(all_news, 1):
        title = news.select_one("h2.title-heading")
        link = news.select_one("a[href]")
        image = news.select_one("div.featured-image-global img")
        author = news.select_one("div.listing-author a")
        time_text = news.select_one("div.listing-author span")
        summary = news.select_one("p")

        raw_time = time_text.get_text(strip=True) if time_text else ""
        parsed_time = ""
        match = re.search(r'Updated\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', raw_time)
        if match:
            try:
                dt = datetime.strptime(match.group(1), "%B %d, %Y")
                parsed_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

        article = {
            "title": title.get_text(strip=True) if title else "",
            "link": link['href'] if link else "",
            "thumbnail_image": image['data-src'] if image else "",
            "author": author.get_text(strip=True) if author else "",
            "time": parsed_time,
        }
        print(f"[LIST] #{i} Parsed: {article['title']}")
        news_list.append(article)

    print(f"[INFO] Found {len(news_list)} articles.")
    return news_list

async def fetch_detail(session: aiohttp.ClientSession, article: dict):
    async with semaphore:
        try:
            print(f"[FETCH] Starting: {article['link']}")
            async with session.get(article['link'], headers=headers, timeout=30,ssl=False) as res:
                html = await res.text()
                soup = BeautifulSoup(html, 'lxml')

                main_img = soup.select_one("div.story-featuredimage img")
                article["main_image"] = main_img['src'] if main_img else ""

                body = soup.select_one("span.story-text")
                if body:
                    cleaned = clean_html_content(body)
                    article["content"] = cleaned.decode_contents()
                else:
                    article["content"] = ""

                print(f"[FETCHED] Done: {article['title']}")

        except Exception as e:
            article["main_image"] = ""
            article["content"] = ""
            print(f"[ERROR] Failed to fetch {article['link']} -> {e}")

async def run_all(news_list):
    print(f"[INFO] Fetching details for {len(news_list)} articles...")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_detail(session, article) for article in news_list]
        await asyncio.gather(*tasks)
    print("[INFO] All article details fetched.")

if __name__ == "__main__":
    print("[START] Tribune Scraper Started")

    news_list = get_news_list()
    asyncio.run(run_all(news_list))

    print("[SAVE] Writing results to data.json...")
    with open('tribune_en.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print("[DONE] All done. Output saved to data.json")