import cloudscraper
import asyncio
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import json

BASE_URL = "https://www.samaa.tv/latest-news"

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)

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

def parse_datetime(raw_time):
    try:
        dt = datetime.strptime(raw_time.strip(), "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""

# Semaphore to limit concurrent requests
semaphore = asyncio.Semaphore(10)

async def fetch_detail(article: dict):
    async with semaphore:
        loop = asyncio.get_event_loop()
        try:
            print(f"[FETCH] Fetching article: {article['title']}")
            response = await loop.run_in_executor(None, lambda: scraper.get(article['link']))
            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            article_div = soup.select_one("article.single-article")

            author_tag = article_div.select_one("div.share-bar strong.h4")
            article["author"] = author_tag.get_text(strip=True).replace("| ", "").strip() if author_tag else ""

            time_tag = article_div.select_one("div.share-bar time")
            raw_time = time_tag.get("datetime", "") if time_tag else ""
            article["time"] = parse_datetime(raw_time)

            main_img_tag = article_div.select_one("div.img-frame img")
            article["main_image"] = main_img_tag.get("data-src", "") if main_img_tag else ""

            body = article_div.select_one("div.article-content")
            article["content"] = clean_html_content(body).decode_contents() if body else ""

            print(f"[SUCCESS] Details fetched for: {article['title']}\n")

        except Exception as e:
            article.update({"author": "", "time": "", "main_image": "", "content": ""})
            print(f"[ERROR] Failed to fetch details for '{article['link']}' -> {e}\n")

def get_news_list():
    res = scraper.get(BASE_URL)
    print(f"[INFO] Response status: {res.status_code}")

    soup = BeautifulSoup(res.text, 'lxml')
    all_news = soup.select("section.story-section article.story-article")
    print(f"[INFO] Found {len(all_news)} news articles.\n")

    news_list = []
    for i, news in enumerate(all_news, 1):
        title_tag = news.select_one("h3")
        short_desc = news.select_one("p")
        link_tag = news.select_one("a")
        img_tag = link_tag.select_one("img") if link_tag else None

        article = {
            "title": title_tag.get_text(strip=True) if title_tag else "",
            "short_desc": short_desc.get_text(strip=True) if short_desc else "",
            "link": link_tag["href"] if link_tag else "",
            "thumbnail_image": img_tag.get("data-src", "") if img_tag else ""
        }
        print(f"[INFO] Article {i}: {article['title']}")
        news_list.append(article)

    return news_list

async def run_all(news_list):
    print(f"[INFO] Starting fetch for {len(news_list)} articles...\n")
    tasks = [fetch_detail(article) for article in news_list]
    await asyncio.gather(*tasks)
    print("[INFO] All article details fetched.\n")

if __name__ == "__main__":
    print(f"[START] Scraper started for {BASE_URL}\n")
    news_list = get_news_list()
    asyncio.run(run_all(news_list))
    print("[SAVE] Saving results\n")
    with open('samaa_en.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
# some comment