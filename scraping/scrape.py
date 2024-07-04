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

links = [
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/obra-nueva/alhaurin-de-la-torre/20422573/183273313?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/obra-nueva/manresa/19868768/164168154?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/madrid-capital/calefaccion-ascensor/181345161/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/madrid-capital/aire-acondicionado-calefaccion-parking-terraza-trastero-ascensor-amueblado/182283713/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/cubelles/aire-acondicionado-calefaccion-parking-terraza-trastero-zona-comunitaria-ascensor-piscina/183510644/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/sitges/aire-acondicionado-calefaccion-parking-terraza-trastero-ascensor-piscina/182197539/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/barcelona-capital/aire-acondicionado-calefaccion-jardin-terraza-ascensor-patio-piscina/183047454/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/sant-cugat-del-valles/aire-acondicionado-calefaccion-parking-terraza-zona-comunitaria-ascensor-piscina/183306043/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/calefaccion-parking-terraza-trastero-ascensor-patio/183534352/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-terraza-ascensor-patio/183740922/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/calefaccion-terraza-ascensor/183680219/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-ascensor/183675474/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-ascensor/183616887/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-trastero-ascensor/183375637/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/calefaccion-terraza-ascensor/183345715/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-terraza-trastero-zona-comunitaria-ascensor-piscina/182962203/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/vallirana/parking-jardin-terraza-television-internet/182846956/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-terraza-ascensor/183629506/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/barcelona-capital/aire-acondicionado-calefaccion-parking-trastero-ascensor/181799257/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-terraza-zona-comunitaria-ascensor-piscina/183150423/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/madrid-capital/aire-acondicionado-calefaccion-ascensor/183721771/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/madrid-capital/aire-acondicionado-calefaccion-terraza-ascensor/182237331/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/madrid-capital/aire-acondicionado-calefaccion-ascensor/182227043/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/madrid-capital/aire-acondicionado-calefaccion-terraza-ascensor/179448779/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/salamanca-capital/calefaccion-terraza-trastero-ascensor/182178138/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-jardin-terraza-trastero-ascensor-piscina/183339929/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/aire-acondicionado-calefaccion-parking-terraza-patio-piscina/183255779/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/barcelona-capital/aire-acondicionado-calefaccion-jardin/183593135/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/barcelona-capital/aire-acondicionado-calefaccion-ascensor/179554785/d?from=list', 
    'https://www.fotocasa.eshttps://www.fotocasa.es/es/comprar/vivienda/granada-capital/calefaccion-terraza/183695145/d?from=list']