import requests
from bs4 import BeautifulSoup as bs
import re
import concurrent.futures
import json

base_url = "https://www.fotocasa.es"
url = f"https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/{1}"
api_url = "https://web.gw.fotocasa.es/v2/propertysearch/search/propertycoordinates?combinedLocationIds=724,0,0,0,0,0,0,0,0&culture=es-ES&includePurchaseTypeFacets=false&isMap=false&isNewConstructionPromotions=false&latitude=40&longitude=-4&pageNumber=1&platformId=1&propertyTypeId=2&size=300&sortOrderDesc=true&sortType=scoring&transactionTypeId=1"
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'referer': 'https://www.fotocasa.es/',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

res = requests.request("GET", api_url, headers=headers)
res = res.json()
print(len(res.get("propertyCoordinates")))
main_list = []
for prop in res.get("propertyCoordinates"):
    prop_dict = {}
    prop_dict.update({"propertyId": prop["propertyId"]}) #prop_id
    prop_dict.update({"coordinates": {"latitude": prop["coordinates"]["latitude"], "longitude": prop["coordinates"]["longitude"]}}) #lat_long
    prop_dict.update({"price": prop["price"]}) #price
    main_list.append(prop_dict)
    
print(main_list)
r = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': 'f1bd630d-7af0-4123-b4dd-6c8010bed171',
        'url': url,
        'bypass': 'cloudflare_level_2',
    },
)
print(r.status_code)
soup = bs(r.content, "html.parser")
# print(soup.prettify())
articles = soup.find("section", class_="re-SearchResult").find_all("article")
print(len(articles))
links = [base_url+a.find("a").get('href') for a in articles]
print(links)