import asyncio
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import json
import re
from playwright.async_api import async_playwright
import time

BASE_URL = "https://www.dawnnews.tv/latest-news"
urdu_months = {
    "جنوری": "January", "فروری": "February", "مارچ": "March",
    "اپریل": "April", "مئ": "May", "مئی": "May", "جون": "June",
    "جولائی": "July", "جولائ": "July", "اگست": "August", "ستمبر": "September",
    "اکتوبر": "October", "نومبر": "November", "دسمبر": "December"
}

patterns = [
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}(?:\s+\d{1,2}:\d{2}(?:am|pm))?",
    r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}(?:\s+\d{1,2}:\d{2}(?:am|pm))?",
]

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

def extract_datetime(raw):
    if not raw: return ""
    raw = re.sub("|".join(urdu_months), lambda m: urdu_months[m.group()], raw)
    raw = re.sub(r"(شائع|اپ ڈیٹ)", "", raw, flags=re.I)
    raw = re.sub(r"(\d{4})(\d{1,2}:\d{2}(?:am|pm))", r"\1 \2", raw.strip())
    raw = re.sub(r"\s+", " ", raw)
    dates = re.findall(r"((January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})", raw)
    if len(dates) > 1: raw = raw.replace(dates[0][0] * 2, dates[0][0])
    # print(raw)
    for p in patterns:
        match = re.search(p, raw, re.I)
        if match:
            for fmt in ["%B %d, %Y %I:%M%p", "%d %B %Y %I:%M%p", "%B %d, %Y", "%d %B %Y"]:
                try:
                    extracted = datetime.strptime(match.group(), fmt).strftime("%Y-%m-%d %H:%M:%S")
                    # print(extracted)
                    return extracted
                except: continue
    return ""

async def fetch_detail(browser, article, i):
    page = await browser.new_page()
    try:
        print(f"[INFO] Fetching details for article #{i}")
        await page.goto(article["link"])
        html = await page.content()
        soup = BeautifulSoup(html, 'lxml')

        author = soup.select_one("span.story__byline")
        article["author"] = author.get_text(strip=True) if author else ""

        time_text = soup.select_one("span.story__time")
        raw_time = time_text.get_text(strip=True) if time_text else ""
        article["time"] = extract_datetime(raw_time)

        main_img = soup.select_one("div.slideshow div.media__item img")
        article["main_image"] = main_img["src"] if main_img else ""

        content = soup.select_one("div.story__content")
        article["content"] = clean_html_content(content).decode_contents() if content else ""

        print(f"[SUCCESS] #{i}: Fetched '{article['title']}'")

    except Exception as e:
        article.update({"author": "", "time": "", "main_image": "", "content": ""})
        print(f"[ERROR] #{i} Failed to fetch {article['link']} -> {e}")

    finally:
        await page.close()

async def scrape():
    print("[INFO] Launching browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"[INFO] Navigating to {BASE_URL}")
        await page.goto(BASE_URL)
        html = await page.content()
        soup = BeautifulSoup(html, 'lxml')
        await page.close()

        articles = soup.select("div.tabs__pane.active article")
        print(f"[INFO] Found {len(articles)} articles on the listing page.")

        news_list = []
        for i, art in enumerate(articles, 1):
            title_tag = art.select_one("h2.story__title")
            link_tag = art.select_one("a.story__link")
            image_tag = art.select_one("div.media__item a img")

            article = {
                "title": title_tag.get_text(strip=True) if title_tag else "",
                "link": link_tag["href"] if link_tag else "",
                "thumbnail_image": image_tag["src"] if image_tag else ""
            }

            news_list.append(article)

        for i, article in enumerate(news_list, 1):
            await fetch_detail(browser, article, i)

        await browser.close()
        print("[INFO] Browser closed.")
        return news_list

def main_dawnnews_ur():
    start_time = time.time()
    news_list = asyncio.run(scrape())

    with open("dawnnews_ur.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

    end_time = time.time()
    print(f"[INFO] Scraping complete. Saved to dawnnews_ur.json")
    print(f"[INFO] Total time taken: {end_time - start_time:.2f} seconds")

main_dawnnews_ur()