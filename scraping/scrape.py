import requests
from bs4 import BeautifulSoup
# from urllib.request import urlopen

# Instagram account scraping

# url = "https://www.instagram.com/programming"
# page = urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# print(soup.prettify())

# data = soup.find("meta", property="og:description")['content']
# print(data)

# Greatest Books org

url = "https://thegreatestbooks.org/"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
# print(soup.prettify())
# tag = soup.html
# print(tag.name)
# tag2 = soup.div
# print(tag2.attrs)
# print(tag2.contents)
# print(tag2.string)
print(soup.find_all("a"))