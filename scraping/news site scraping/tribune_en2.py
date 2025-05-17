import requests
from bs4 import BeautifulSoup as bs
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

r = requests.get('https://tribune.com.pk/latest')
# print(r.status_code)

soup = bs(r.content, 'html.parser')
# print(soup.prettify())
article_data = []

home_div = soup.find(class_='home')
li_elements = home_div.find('div', id='all').find_all('li')
        
for i, li in enumerate(li_elements):
    source_link = li.find('a')['href'] if li.find('a') else None
    title = li.find('h2').get_text(strip=True) if li.find('h2') else None
    author = li.find(class_='listing-author').find('a').get_text(strip=True) if li.find(class_='listing-author') else None
    if li.find('img'):
        thumbnail = li.find('img')['src']
        thumb_path = f"media/thumbnail_{i+1}.jpg"
        with open(thumb_path, 'wb') as f:
            f.write(requests.get(thumbnail).content)
    else: thumbnail = None
    # print(source_link, title, thumbnail, sep="\n")
    article_data.append({
        "source_link": source_link,
        "title": title,
        "thumbnail": thumbnail
    })

    if not source_link:
        continue

def process_detail_page(article):
    source_link = article["source_link"]
    title = article['title']
    thumbnail = article['thumbnail']
    if not source_link:
        return
    detail_page_res = requests.get(source_link)
    print(detail_page_res.status_code)
    soup = bs(detail_page_res.content, 'html.parser')
    content_div = soup.find(class_='mainstorycontent-parent')
    # print(content_div)
    if content_div:
        detail_page_image = content_div.find(class_="top-big-img").find("img")['src'] if content_div.find(class_="top-big-img") else None
        story_text = str(content_div.find(class_='story-text')) if content_div.find(class_='story-text') else None
        # print(detail_page_image)
        # print(story_text)

        detail_img_path = f"media/detail_image_{i+1}.jpg"
        with open(detail_img_path, 'wb') as f:
            f.write(requests.get(detail_page_image).content)
        
        return {
            "source_link": source_link,
            "title": title,
            "thumbnail": thumbnail,
            "author": "",
            "date_posted": "",
            "detail_page_image": detail_page_image,
            "story_text": story_text
        }

articles = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_detail_page, article) for article in article_data]
    for future in as_completed(futures):
        result = future.result()
        if result:
            articles.append(result)

with open("tribune_en.json", "w", encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)