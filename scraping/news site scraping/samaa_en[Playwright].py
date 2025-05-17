import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import json
import time

BASE_URL = "https://www.samaa.tv/latest-news"

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
        dt = datetime.strptime(raw_time, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""

async def fetch_detail(browser, article, i):
    page = await browser.new_page()
    try:
        print(f"[INFO] Fetching details for article #{i}: {article['title']}")
        await page.goto(article["link"])
        await page.locator("article.single-article").first.wait_for()
        html = await page.content()
        soup = BeautifulSoup(html, 'lxml')

        article_div = soup.select_one("article.single-article")
        author_tag = article_div.select_one("div.share-bar strong.h4")
        article["author"] = author_tag.get_text(strip=True).replace("| ", "").strip() if author_tag else ""

        time_tag = article_div.select_one("div.share-bar time")
        raw_time = time_tag.get("datetime", "") if time_tag else ""
        print(raw_time)
        article["time"] = parse_datetime(raw_time)

        main_img_tag = article_div.select_one("div.img-frame img")
        article["main_image"] = main_img_tag.get("data-src", "") if main_img_tag else ""

        body = article_div.select_one("div.article-content")
        article["content"] = clean_html_content(body).decode_contents() if body else ""

        print(f"[SUCCESS] #{i}: Details fetched for '{article['title']}'")

    except Exception as e:
        article.update({"author": "", "time": "", "main_image": "", "content": ""})
        print(f"[ERROR] #{i} Failed to fetch {article['link']} -> {e}")

    finally:
        await page.close()


async def scrape():
    async with async_playwright() as p:
        print("[INFO] Launching browser...")
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print(f"[INFO] Navigating to {BASE_URL}")
        await page.goto(BASE_URL)
        await page.locator("section.story-section").first.wait_for(timeout=30000)
        soup = BeautifulSoup(await page.content(), "lxml")
        await page.close()

        articles = soup.select("section.story-section article.story-article")
        print(f"[INFO] Found {len(articles)} articles.")

        news_list = []
        for i, art in enumerate(articles, 1):
            title_tag = art.select_one("h3")
            link_tag = art.select_one("a")
            img_tag = link_tag.select_one("img") if link_tag else None

            article = {
                "title": title_tag.get_text(strip=True) if title_tag else "",
                "link": link_tag["href"] if link_tag else "",
                "thumbnail_image": img_tag.get("data-src", "") if img_tag else ""
            }
            news_list.append(article)

        print("[INFO] Starting sequential detail fetch for each article...")
        for i, article in enumerate(news_list, 1):
            await fetch_detail(browser, article, i)

        await browser.close()
        print("[INFO] Browser closed.")

        with open("samaa_en.json", "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
        print("[DONE] All articles saved to samaa_en.json.")

if __name__ == "__main__":
    start_time = time.time()
    print(f"[START] Scraper Started for {BASE_URL}")
    asyncio.run(scrape())
    end_time = time.time()
    print(f"[INFO] Total time taken: {end_time - start_time:.2f} seconds")