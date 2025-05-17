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
BASE_URL = "https://www.nation.com.pk/latest"
semaphore = asyncio.Semaphore(10)

def get_news_list():
    # print("[INFO] Fetching latest news list...")
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    all_news = soup.select("div.jeg_posts_wrap article")
    news_list = []

    for i, news in enumerate(all_news, 1):
        link = news.select_one("a[href]")
        link = link['href'] if link else ""
        if "cartoon" in link.lower():
            continue
        div = news.select_one("div.thumbnail-container div")
        style = div.get("style", "")
        if style:
            # Extract the URL using regex
            match = re.search(r"background-image:\s*url\(['\"]?(.*?)['\"]?\)", style)
            image = match.group(1) if match else ""
        else: image = ""

        article = {
            "link": link,
            "thumbnail_image": image,
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

                title = soup.select_one("h1.jeg_post_title")
                article["title"] = title.get_text(strip=True) if title else ""
                author = soup.select_one("div.jeg_meta_author")
                article["author"] = author.get_text(strip=True) if author else ""
                time_text = soup.select_one("div.jeg_meta_date")
                raw_time = time_text.get_text(strip=True).replace("|", "").strip() if time_text else ""
                try:
                    dt = datetime.strptime(raw_time, "%I:%M %p %B %d, %Y")
                    article["time"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    article["time"] = ""

                main_img = soup.select_one("div.detail-page-main-image img")
                article["main_image"] = main_img['src'] if main_img else ""

                body = soup.select_one("div.news-detail-content-class")
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
            # print(f"[ERROR] Failed to fetch {article['link']} -> {e}")

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
    with open('nation_en.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print("[DONE] All done. Output saved")