import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from datetime import datetime
import json
import re, time
import asyncio
import aiohttp
from bs4 import Comment, Doctype

def clean_html_content(element):
    for tag in element.find_all(["script", "style", "iframe", "noscript"]):
        tag.decompose()
    for div in element.find_all("div"):
        if not div.get_text(strip=True) and not div.find(["img", "a", "p", "strong", "em"]):
            div.decompose()
    for comment in element.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    for item in element.contents:
        if isinstance(item, Doctype):
            item.extract()
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
BASE_URL = "https://urdu.geo.tv/latest-news"
semaphore = asyncio.Semaphore(10)

urdu_months = {
    "جنوری": "January", "فروری": "February", "مارچ": "March",
    "اپریل": "April", "مئ": "May", "مئی": "May", "جون": "June",
    "جولائی": "July", "جولائ": "July", "اگست": "August", "ستمبر": "September",
    "اکتوبر": "October", "نومبر": "November", "دسمبر": "December"
}

def parse_urdu_date(raw_time):
    try:
        raw_time = raw_time.replace("،", "").strip()
        parts = raw_time.split()
        day, month_raw, year = parts
        month_clean = re.sub(r"[^A-Za-zآ-ی]+", "", month_raw)
        month = urdu_months.get(month_clean, month_clean)
        formatted = f"{month} {day}, {year}"
        dt = datetime.strptime(formatted, "%B %d, %Y")
        parsed_date = dt.strftime("%Y-%m-%d")
        return parsed_date
    except Exception as e:
        return ""

def get_news_list():
    print("[INFO] Fetching latest news list...")
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    first_news = soup.select_one("div.FirstBlock")
    all_news = soup.select("div.singleBlock")
    if first_news:
        all_news.insert(0, first_news)
    print(f"[INFO] Found {len(all_news)} news blocks.")

    news_list = []

    for i, news in enumerate(all_news, 1):
        link = news.select_one("a[href]")
        title = news.select_one("div.entry-title h2") or news.select_one("div.entry-title h1")
        short_desc = news.select_one("p")
        image = news.select_one("div.pic img")
        time_text = news.select_one("div.entry-title span.date")
        raw_time = time_text.get_text(strip=True) if time_text else ""
        time = parse_urdu_date(raw_time)

        article = {
            "title": title.get_text(strip=True) if title else "",
            "short_desc": short_desc.get_text(strip=True) if short_desc else "",
            "link": link['href'] if link else "",
            "thumbnail_image": image['data-src'] if image else "",
            "time": time,
        }
        news_list.append(article)

    print(f"[INFO] Found {len(news_list)} articles.")
    return news_list

async def fetch_detail(session: aiohttp.ClientSession, article: dict):
    async with semaphore:
        try:
            # print(f"[DETAIL] Fetching: {article['link']}")
            async with session.get(article['link'], headers=headers, timeout=30, ssl=False) as res:
                print(f"Status code: {res.status}")
                html = await res.text()
                soup = BeautifulSoup(html, 'lxml')

                short_desc = soup.select_one("div.excerpt-full")
                article["short_desc"] = short_desc.get_text(strip=True) if short_desc else ""

                author = soup.select_one("span.author_agency")
                article["author"] = author.get_text(strip=True) if author else ""

                main_img = soup.select_one("div.content-area div.medium-insert-images img") or soup.select_one("div.full-cover-img img")
                article["main_image"] = main_img['src'] if main_img else ""

                content = soup.select_one("div.content-area") or soup.select_one("div.story-detail")
                if content:
                    image_div = content.select_one("div.medium-insert-images")
                    if image_div:
                        image_div.decompose()

                article["content"] = clean_html_content(content).decode_contents() if content else ""
                print(f"[FETCHED] Done: {article['title']}")

        except Exception as e:
            article.update({"author": "", "main_image": "", "content": ""})
            print(f"[ERROR] Failed to fetch {article['link']} -> {e}")

async def run_all(news_list):
    print(f"[ASYNC] Fetching details for {len(news_list)} articles...")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_detail(session, article) for article in news_list]
        await asyncio.gather(*tasks)
    print("[ASYNC] All article details fetched.")


def main_geonews_ur():
    start_time = time.time()
    print(f"[START] Scraper Started for {BASE_URL}")

    news_list = get_news_list()
    print("[INFO] Starting async detail fetch...")
    asyncio.run(run_all(news_list))

    print("[SAVE] Writing results...")
    with open('geonews_ur.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"[INFO] Total time taken: {total_time:.2f} seconds")

main_geonews_ur()