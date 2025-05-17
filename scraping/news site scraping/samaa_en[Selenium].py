from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import Comment
import json, datetime, time

options = webdriver.ChromeOptions()
custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={custom_user_agent}")
# options.add_argument("--headless=chrome")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
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

def get_news_list():
    driver.get(BASE_URL)
    # print(driver.page_source)

    articles = driver.find_elements(By.CSS_SELECTOR, "section.story-section article.story-article")
    print(f"[INFO] Found {len(articles)} articles.")
    news_list = []
    for i, news in enumerate(articles, 1):
        title_tag = news.find_element(By.TAG_NAME, "h3")
        link_tag = news.find_element(By.TAG_NAME, "a")
        img_tag = link_tag.find_element(By.TAG_NAME, "img") if link_tag else None

        article = {
            "title": title_tag.text.strip() if title_tag else "",
            "link": link_tag.get_attribute("href") if link_tag else "",
            "thumbnail_image": img_tag.get_attribute("data-src") if img_tag else ""
        }
        news_list.append(article)
        # print(len(news_list))
    return news_list

def fetch_detail(article, i):
    driver.get(article['link'])
    # print(driver.page_source)
    try:
        article_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.single-article")))
        # article_div = driver.find_element(By.CSS_SELECTOR, "article.single-article")
        author_tag = article_div.find_element(By.CSS_SELECTOR, "div.share-bar strong.h4")
        article["author"] = author_tag.text.replace("| ", "").strip() if author_tag else ""

        time_tag = article_div.find_element(By.CSS_SELECTOR, "div.share-bar time")
        raw_time = time_tag.get_attribute("datetime") if time_tag else ""
        # print(raw_time)
        article["time"] = parse_datetime(raw_time)

        main_img_tag = article_div.find_element(By.CSS_SELECTOR, "div.img-frame img")
        article["main_image"] = main_img_tag.get_attribute("data-src") if main_img_tag else ""

        body = article_div.find_element(By.CSS_SELECTOR, "div.article-content")
        article["content"] = clean_html_content(body).decode_contents() if body else ""

        print(f"[SUCCESS] #{i}: Details fetched for '{article['title']}'")
    except Exception as e:
        article.update({"author": "", "time": "", "main_image": "", "content": ""})
        print(f"[ERROR] #{i} Failed to fetch {article['link']} -> {e}")

def main_samaa_en():
    start_time = time.time()
    news_list = get_news_list()
    for i, article in enumerate(news_list[:5], 1):
        fetch_detail(article, i)

    driver.quit()
    with open("samaa_en.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print("[DONE] All articles saved.")
    end_time = time.time()
    print(f"[INFO] Total time taken: {end_time - start_time:.2f} seconds")

main_samaa_en()